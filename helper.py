from nltk.corpus import wordnet as wn

# Get the similarity of two words
# We get it by taking the maximal similarity we can get when looking at both synsets
def get_wordnet_similarity(word1, word2):
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

# Returns the surrounding text of an event
def get_surrounding(textfile, dirname, event_begin, event_end, words_left, words_right):
    with open(dirname+"/"+textfile, "r") as f:
        f.seek(event_begin)
        left = get_surrounding_words(f, "left", words_left)

def get_surrounding_words(file, direction, n_words):
    if direction == "left":
        steps = 0
        going_left = True

        for i in range(n_words+1):
            # Go left until we hit a space, newline or the beginning of the textfile
            going_left = True
            while going_left:
                # Can't go further
                if file.tell() == 0:
                    going_left = False
                    break

                # Go one left
                file.seek(file.tell()-1)
                steps += 1

                # Go to next word
                c = file.read(1)
                if c == ' ' or c == '\n':
                    going_left = False
                # file.read(1) moves forward, so we have to go back
                file.seek(file.tell()-1)

        return file.read(steps).strip()

    if direction == "right":
        steps = 0
        going_right = True
        text = ""

        for i in range(n_words+1):
            # Go right until we hit a space or a newline
            going_right = True
            while going_right:
                c = file.read(1)
                if c == ' ' or c == '\n' or c == '':
                    going_right = False

                text = text + c
            print "word"

        return text


