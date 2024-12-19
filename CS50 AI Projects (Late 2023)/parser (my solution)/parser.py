import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj Clause

Clause -> VP | NP VP

NP -> N | Det NP | AP NP | NP PP
VP -> VPE | VPE NP | VPE PP | VPE NP Advs | VPE PP Advs
VPE -> V | V Advs | Adv VPE
Advs -> Adv | Advs
AP -> Adj | Adj AP
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Convert all characters in sentence into lowercase and convert sentence into list of words
    sentence_list = nltk.tokenize.word_tokenize(sentence.lower())

    # Remove any word that does not contain at least one alphabetic character from list of words
    for word in sentence_list:
        contains_alpha = False
        for char in word:
            if char.isalpha():
                contains_alpha = True

        if not contains_alpha:
            sentence_list.remove(word)

    return sentence_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    noun_phrase_chunk_list = []

    # Add all noun phrases in sentence into "pending" list
    pending = get_noun_phrases(tree)

    # For each tree in "pending", if tree does not contain any noun phrases, add tree to noun_phrase_chunk_list
    for pending_tree in pending:
        if len(get_noun_phrases(pending_tree)) == 0:
            noun_phrase_chunk_list.append(pending_tree)

    return noun_phrase_chunk_list


def get_noun_phrases(tree):

    # pending serves as a queue to ensure that we run through every "node"/subtree in the main tree
    pending = [tree]

    # noun_phrases is a list that collates all the noun_phrases found in the main tree
    noun_phrases = []

    # While length of queue > 0
    while len(pending) != 0:
        # Remove an element from the queue
        current_tree = pending[0]
        pending.pop(0)

        # Add all the subtrees of the current tree into the queue
        # Add subtree into noun_phrases if subtree is a noun phrase itself
        if type(current_tree) != str:
            for subtree in current_tree:
                if type(subtree) != str:
                    pending.append(subtree)
                    if subtree.label() == "NP":
                        noun_phrases.append(subtree)

    return noun_phrases


if __name__ == "__main__":
    main()
