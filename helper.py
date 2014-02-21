import string
import numpy
from cStringIO import StringIO
import re

# Preprocessing of sentence
def preprocess_sentence(text):
        def repl(m):
            return m.group(1) + " " + m.group(2)
        # Removing newlines
        text_tmp = re.sub(r"(\w+)\n(\w+)", repl, text)
        text_tmp = re.sub(r"$\n", "", text_tmp)

        # Removing everything between two words and replacing it by a space
        text_tmp = re.sub(r"(\w+)\W*[,\";:]+\W*(\w+)", repl, text_tmp)
        # Run again because re.sub only matches non overlapping stuff. "you, pray," -> "you pray,"
        text_tmp = re.sub(r"(\w+)\W*[,\";:]+\W*(\w+)", repl, text_tmp)

        # Removing "--" but not "-" between two words ("to-do")
        text_tmp = re.sub(r"(\w+)\W*--\W*(\w+)", repl, text_tmp)

        # Replaceing "'" only when there is a space next to it. Not replacing "don't" by "don t"
        text_tmp = re.sub(r"(\w+)\W+'+\W*(\w+)", repl, text_tmp)
        text_tmp = re.sub(r"(\w+)\W*'+\W+(\w+)", repl, text_tmp)

        # Removing sentences endings (?!.)
        text_tmp = text_tmp.strip(".").strip("?").strip("!").strip(";").strip(":").strip('"').strip()
        return text_tmp


# Returns the sentence the event is in
def get_sentence(event_text, textfile, dirname, event_begin):
    with open(dirname+"/"+textfile, "r") as f:
        # Read the text left of the event
        f.seek(event_begin)
        begin = go_left_until_point(f)

        # Read the text right of the event
        f.seek(event_begin)
        end = go_right_until_point(f)

        # Look how many words with the same text of the event are in front of the event we are interested in
        same_words_before_event = count_words(f, event_text, event_begin, begin)

        # Return the sentence
        f.seek(begin)
        return (f.read(end-begin).strip(".").strip(), same_words_before_event)

def count_words(f, event_text, event_begin, text_begin):
    f.seek(text_begin)

    tmp = ""
    count = 0
    while f.tell() < event_begin:
        c = f.read(1)
        if c == event_text[0]:
            tmp = c + f.read(len(event_text)-1)
            if tmp == event_text:
                # Case: fell - felling
                c = f.read(1)
                if c == " " or c == "-":
                    count += 1
            tmp = ""

    return count

# Returns the surrounding text of an event (event included in text)
def get_surrounding(event_text, textfile, dirname, event_begin, words_left, words_right):
    sentence, same_words_before_event = get_sentence(event_text, textfile, dirname, event_begin)

    # Remove everything which is not a word
    sentence = preprocess_sentence(sentence)

    # Turn sentence into a list of words
    words = sentence.split()

    # Getting the index of the event
    index = None
    count = 0
    for i, word in enumerate(words):
        if word == event_text:
            if count == same_words_before_event:
                index = i
                break
            count += 1

    # Returning the surrounding area
    if (index-words_left) >= 0:
        return string.join(words[(index-words_left):(index+words_right+1)], " ")
    else:
        return string.join(words[0:(index+words_right+1)], " ")

def go_left_until_point(f):
    c = f.read(1)
    f.seek(f.tell()-1)
    while c != "." and c != "?" and c != "!" and f.tell() != 0:
        # Go back one character
        f.seek(f.tell()-1)
        c = f.read(1)
        f.seek(f.tell()-1)

    return f.tell()

def go_right_until_point(f):
    c = f.read(1)
    while c != "." and c != "?" and c != "!" and c != "":
        c = f.read(1)

    return f.tell()

def get_stem_class(stems, stem):
    return numpy.where(stems==stem)[0][0]
