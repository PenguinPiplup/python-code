import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Sort everyone according to whether their parents are known
    known_parents = set()
    unknown_parents = set()
    for person in people:
        if people[person]["mother"] == None:
            unknown_parents.add(person)
        else:
            known_parents.add(person)

    # Variable which will contain the joint probability to be returned
    joint_prob = 1

    # Iterate over all the people with unknown parents and update joint probability
    for person in unknown_parents:
        if person in one_gene:
            joint_prob *= PROBS["gene"][1]
            joint_prob *= PROBS["trait"][1][person in have_trait]
        elif person in two_genes:
            joint_prob *= PROBS["gene"][2]
            joint_prob *= PROBS["trait"][2][person in have_trait]
        else:
            joint_prob *= PROBS["gene"][0]
            joint_prob *= PROBS["trait"][0][person in have_trait]

    # Iterate over all the people with known parents and update joint probability
    for person in known_parents:
        # Store name of parents
        mother = people[person]["mother"]
        father = people[person]["father"]

        # Calculate and store probability of inheriting a gene from mother
        if mother in two_genes:
            p_inherit_from_mum = 1 - PROBS["mutation"]
        elif mother in one_gene:
            p_inherit_from_mum = 0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])
        else:
            p_inherit_from_mum = PROBS["mutation"]

        # Calculate and store probability of inheriting a gene from father
        if father in two_genes:
            p_inherit_from_dad = 1 - PROBS["mutation"]
        elif father in one_gene:
            p_inherit_from_dad = 0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])
        else:
            p_inherit_from_dad = PROBS["mutation"]

        # Find the number of genes the person has in this specific scenario
        # Find probability that person has "child" number of genes (with mutations considered)
        if person in two_genes:
            child = 2
            joint_prob *= (p_inherit_from_mum * p_inherit_from_dad)
        elif person in one_gene:
            child = 1
            joint_prob *= (p_inherit_from_mum * (1 - p_inherit_from_dad) + p_inherit_from_dad * (1 - p_inherit_from_mum))
        else:
            child = 0
            joint_prob *= ((1 - p_inherit_from_mum) * (1 - p_inherit_from_dad))

        # Find and update probability that person has/does not have trait, given that person has "child" number of genes
        joint_prob *= PROBS["trait"][child][person in have_trait]

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Iterate over every person, updating their gene and trait distributions
    for person in probabilities:
        # Update gene distributions for that person
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        # Update trait distributions for that person
        probabilities[person]["trait"][person in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # Iterate over every person, normalising their gene and trait probability distributions
    for person in probabilities:
        # Normalise person's gene distribution
        tmpsum_gene = probabilities[person]["gene"][2] + probabilities[person]["gene"][1] + probabilities[person]["gene"][0]
        multiplier_gene = 1 / tmpsum_gene
        for i in range(3):
            probabilities[person]["gene"][i] *= multiplier_gene

        # Normalise person's trait distribution
        tmpsum_trait = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        multiplier_trait = 1 / tmpsum_trait
        probabilities[person]["trait"][True] *= multiplier_trait
        probabilities[person]["trait"][False] *= multiplier_trait


if __name__ == "__main__":
    main()
