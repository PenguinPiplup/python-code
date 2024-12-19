from logic import *


AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Knowledge base that applies to all puzzles
knowledgebase = And()

for tup in [(AKnight, AKnave), (BKnight, BKnave), (CKnight, CKnave)]:
    knowledgebase.add(Implication(tup[0], Not(tup[1])))
    knowledgebase.add(Implication(tup[1], Not(tup[0])))

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    Or(And(AKnight, AKnave, AKnight), And(AKnave, Not(And(AKnight, AKnave)))),
    knowledgebase
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    Or(And(AKnight, AKnave, BKnave), And(AKnave, Not(And(AKnave, BKnave)))),
    Or(BKnight, BKnave),
    knowledgebase
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

# Listing out the possible scenarios for A and B being the same kind
same_kind = Or(And(AKnight, BKnight), And(AKnave, BKnave))
# Listing out the possible scenarios for A and B being of different kind
different_kind = Or(And(AKnight, BKnave), And(AKnave, BKnight))

knowledge2 = And(
    # TODO
    Or(And(AKnight, same_kind), And(AKnave, different_kind)),
    Or(And(BKnight, different_kind), And(BKnave, same_kind)),
    knowledgebase
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And(
    # TODO
    # Adding in last 2 sentences first
    Or(And(BKnight, CKnave), And(BKnave, CKnight)),
    Or(And(CKnight, AKnight), And(CKnave, AKnave)),
    knowledgebase
)

# Combining logic for 'A says either "I am a knight." or "I am a knave." '
EitherOrForA = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))

A_test = Or(And(AKnight, EitherOrForA), And(AKnave, Not(EitherOrForA)))

# Check whether we can determine if A is a Knight or a Knave.
# If there is insufficient info to determine what A is, model_check will return False for both conditions
# If there is sufficient info to determine what A is, A is a knave because A said "but you don't know which"
if model_check(A_test, AKnight) or model_check(A_test, AKnave):
    knowledge3.add(AKnave)

    # If A said that he is a knave, B is a knight
    knowledge3.add(BKnight)

else:
    # If A did not reveal what he is, B is a knave
    knowledge3.add(BKnave)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
