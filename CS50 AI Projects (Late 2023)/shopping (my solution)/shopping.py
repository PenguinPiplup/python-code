import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # Dictionary mapping months to their respective number
    months = {"Jan": 0,
              "Feb": 1,
              "Mar": 2,
              "Apr": 3,
              "May": 4,
              "June": 5,
              "Jul": 6,
              "Aug": 7,
              "Sep": 8,
              "Oct": 9,
              "Nov": 10,
              "Dec": 11}

    evidence = []
    labels = []

    with open(filename) as file:
        reader = csv.DictReader(file)

        # Iterate over each line (user) in file
        for line in reader:

            # line_evidence will collate all of the evidence of that particular line/user
            line_evidence = []

            # Add "Administrative" as an integer
            line_evidence.append(int(line["Administrative"]))

            # Add "Administrative_Duration" as a floating point number
            line_evidence.append(float(line["Administrative_Duration"]))

            # Add "Informational" as an integer
            line_evidence.append(int(line["Informational"]))

            # Add "Informational_Duration" as a floating point number
            line_evidence.append(float(line["Informational_Duration"]))

            # Add "ProductRelated" as an integer
            line_evidence.append(int(line["ProductRelated"]))

            # Add "ProductRelated_Duration" as a floating point number
            line_evidence.append(float(line["ProductRelated_Duration"]))

            # Add "BounceRates" as a floating point number
            line_evidence.append(float(line["BounceRates"]))

            # Add "ExitRates" as a floating point number
            line_evidence.append(float(line["ExitRates"]))

            # Add "PageValues" as a floating point number
            line_evidence.append(float(line["PageValues"]))

            # Add "SpecialDay" as a floating point number
            line_evidence.append(float(line["SpecialDay"]))

            # Add "Month" as an index from 0 (January) to 11 (December)
            line_evidence.append(months[line["Month"]])

            # Add "OperatingSystems" as an integer
            line_evidence.append(int(line["OperatingSystems"]))

            # Add "Browser" as an integer
            line_evidence.append(int(line["Browser"]))

            # Add "Region" as an integer
            line_evidence.append(int(line["Region"]))

            # Add "TrafficType" as an integer
            line_evidence.append(int(line["TrafficType"]))

            # Add "VisitorType", as an integer 0 (not returning) or 1 (returning)
            if line["VisitorType"] == "Returning_Visitor":
                line_evidence.append(1)
            else:
                line_evidence.append(0)

            # Add "Weekend", as an integer 0 (if false) or 1 (if true)
            if line["Weekend"] == "TRUE":
                line_evidence.append(1)
            else:
                line_evidence.append(0)

            # Update evidence
            evidence.append(line_evidence)

            # Update labels, where each label is 1 if Revenue is true, and 0 otherwise.
            if line["Revenue"] == "TRUE":
                labels.append(1)
            else:
                labels.append(0)

    # Return tuple
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Initialise variables and set them to 0
    correct_positives, correct_negatives, total_positives, total_negatives = (0, 0, 0, 0)

    # Iterate over every item in labels
    for comparison in range(len(labels)):

        # If actual label is positive
        if labels[comparison] == 1:
            total_positives += 1
            # If predicted label matches actual label (both positive)
            if predictions[comparison] == 1:
                correct_positives += 1

        # If actual label is negative
        else:
            total_negatives += 1
            # If predicted label matches actual label (both negative)
            if predictions[comparison] == 0:
                correct_negatives += 1

    # Calculate sensitivity and specificity and return them in a tuple
    sensitivity = correct_positives / total_positives
    specificity = correct_negatives / total_negatives

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
