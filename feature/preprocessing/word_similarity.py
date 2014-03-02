from nltk.corpus import wordnet as wn

def get_wordnet_similarity(word1, word2):
    """Returns the similarity of two words.

    We get it by taking the maximum similarity we can get when looking at both synsets.
    """

    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)
    maxSim = None
    for s1 in synsets1:
        for s2 in synsets2:
            # Part of Speech has to be the same
            if s1.pos() != s2.pos():
                continue

            sim = s1.lch_similarity(s2)
            if maxSim == None or maxSim < sim:
                maxSim = sim

    if maxSim:
        return maxSim
    else:
        return 0


