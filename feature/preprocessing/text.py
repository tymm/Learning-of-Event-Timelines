import string
import numpy
from cStringIO import StringIO
import re

def preprocess_sentence(text):
    """Preprocessing of sentences. Removes stuff so word tokenizing gets better. Returns the cleaned up input sentence."""
    def repl(m):
        return m.group(1) + " " + m.group(2)

    # lower everything
    text_tmp = text.lower()

    # Removing newlines
    text_tmp = re.sub(r"(\w+)\n(\w+)", repl, text)
    text_tmp = re.sub(r"$\n", "", text_tmp)

    # Removing everything between two words and replacing it by a space
    text_tmp = re.sub(r"(\w+)\W*[,\";:]+\W*(\w+)", repl, text_tmp)
    # Run again because re.sub only matches non overlapping stuff. "you, pray," -> "you pray,"
    text_tmp = re.sub(r"(\w+)\W*[,\";:]+\W*(\w+)", repl, text_tmp)

    # Removing "--" but not "-" between two words ("to-do")
    text_tmp = re.sub(r"(\w+)\W*--\W*(\w+)", repl, text_tmp)

    # Replaceing "'" only when there is a space next to it. Not replacing "don't" with "don t"
    text_tmp = re.sub(r"(\w+)\W+'+\W*(\w+)", repl, text_tmp)
    text_tmp = re.sub(r"(\w+)\W*'+\W+(\w+)", repl, text_tmp)

    # Replace stuff with apostrophs with the long version for easier chunking and tagging
    text_tmp = text_tmp.replace("doesn't", "does not")
    text_tmp = text_tmp.replace("don't", "do not")
    text_tmp = text_tmp.replace("won't", "will not")
    text_tmp = text_tmp.replace("i'm", "i am")
    text_tmp = text_tmp.replace("isn't", "is not")
    text_tmp = text_tmp.replace("aren't", "are not")
    text_tmp = text_tmp.replace("wasn't", "was not")
    text_tmp = text_tmp.replace("weren't", "were not")
    text_tmp = text_tmp.replace("haven't", "have not")
    text_tmp = text_tmp.replace("hasn't", "has not")
    text_tmp = text_tmp.replace("hadn't", "had not")
    text_tmp = text_tmp.replace("'ll", " will")

    # Removing sentences endings (?!.)
    text_tmp = text_tmp.strip(".").strip("?").strip("!").strip(";").strip(":").strip('"').strip()
    return text_tmp


def get_sentence(event_text, textfile, dirname, event_begin):
    """Returns the sentence the event is in."""
    with open(dirname+"/"+textfile, "r") as f:
        # Read the text left of the event
        f.seek(event_begin)
        begin = go_left_until_point(f)

        # Read the text right of the event
        f.seek(event_begin)
        end = go_right_until_point(f)

        # Look how many words with the same text as the event are in front of the event we are interested in
        same_words_before_event = count_words(f, event_text, event_begin, begin)

        # Return the sentence
        f.seek(begin)

        # Read sentence
        sentence = f.read(end-begin).strip(".").strip()

        # Remove everything which is not a word
        sentence = preprocess_sentence(sentence)

        return sentence, same_words_before_event


def count_words(f, event_text, event_begin, text_begin):
    """Returns the number of words between the begin of the sentence the event is in and the event."""
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

def get_surrounding(event_text, textfile, dirname, event_begin, words_left, words_right):
    """Returns the surrounding text of an event (event included)."""
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
    """Returns the position in the text of the first point when going left."""
    c = f.read(1)
    f.seek(f.tell()-1)
    while c != "." and c != "?" and c != "!" and f.tell() != 0:
        # Go back one character
        f.seek(f.tell()-1)
        c = f.read(1)
        f.seek(f.tell()-1)

    return f.tell()

def go_right_until_point(f):
    """Returns the position in the text of the first point when going right."""
    c = f.read(1)
    while c != "." and c != "?" and c != "!" and c != "":
        c = f.read(1)

    return f.tell()


