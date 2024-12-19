import csv
import sys

def main():
    arg_length = len(sys.argv)
    if arg_length < 3:
        sys.exit("Too few command-line arguments")
    elif arg_length > 3:
        sys.exit("Too many command-line arguments")
    elif not sys.argv[1].endswith(".csv") or not sys.argv[2].endswith(".csv"):
        sys.exit("Must use csv files")

    try:
        students = []
        with open(sys.argv[1]) as file:
            data = csv.DictReader(file)
            for dict in data:
                tmp = dict["name"].split(", ")
                students.append({"first": tmp[1], "last": tmp[0], "house": dict["house"]})
    except FileNotFoundError:
        sys.exit(f"Could not read {sys.argv[1]}")
    else:
        with open(sys.argv[2], "w") as file:
            writer = csv.writer(file)
            writer.writerow(["first", "last", "house"])
            for student in students:
                writer.writerow([student["first"], student["last"], student["house"]])


if __name__ == "__main__":
    main()