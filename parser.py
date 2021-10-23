import sys
import re
import nltk

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

S -> NP VP | S Conj S | PP S

NP -> N | AP NP | N PP | Det NP 
AP -> Adj | Adj AP 
PP -> P NP | P S 
VP -> V | V NP | V NP PP | Adv VP | VP Adv | V PP | VP Conj VP
"""

#       NP
# N          -> Holmes ...
# AP NP      -> ... enigmatical Holmes ...
# N PP       -> ... armchair in the house ...
# Det NP     -> ... the house ...

#       AP
# Adj        -> country ...
# Adj AP     -> red little ...

#       PP
# P NP       -> .. in the house ...
# P S        -> .. at the house Holmes sat down...

#       VP
# V          -> had ...
# V NP       -> had a lit ...
# V NP PP    -> had a lit in the palm ...
# Adv VP     -> never had ...
# VP Adv     -> came here 
# VP Conj VP -> sat and smiled


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
    # Remove punctuation
    sentence = re.sub(r'[^\w\s]', '', sentence)

    # Tokenize and make all lowercase words
    list_of_words = nltk.word_tokenize(sentence.lower())

    return list_of_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # For every single subtree possible for the tree, check either if
    # it is a NP chunk. If it is, add it to the list.
    np_chunks = [subtree for subtree in tree.subtrees(is_np_chunk)]
    
    return np_chunks

def is_np_chunk(tree):
    """
    Accept a tree as an argument.
    Returns True if it is NP chunk. Otherwise, it returns False.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # Get all the NP children of the current tree
    # If the subtree is a NP and it is not itself the current
    # tree, then it adds the NP children to the list
    np_children = list(tree.subtrees(lambda subt: subt.label() == "NP" and subt != tree))

    # If it is NP and does not  have any other NP as children, then it is a NP chunk
    if tree.label() == "NP" and not np_children:
        return True
    else:
        return False



if __name__ == "__main__":
    main()
