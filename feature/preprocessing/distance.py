import os
import cPickle as pickle

def get_distance(event_source_begin, event_target_begin, textfile, dirname):
    """Returns the distance in words for two event."""
    with open(dirname+"/"+textfile, "r") as f:
        if event_source_begin < event_target_begin:
            f.seek(event_source_begin)
            distance = go_right_and_count_words(f, event_target_begin)
        else:
            f.seek(event_target_begin)
            distance = go_left_and_count_words(f, event_source_begin)

    return distance

def go_left_and_count_words(f, until):
    """Returns the distance in words."""
    count = 0
    c = f.read(1)
    f.seek(f.tell()-1)
    while f.tell() != 0 and f.tell() < until:
        # Go back one character
        f.seek(f.tell()-1)

        if c == " " or c == "\n":
            count += 1

        c = f.read(1)
        f.seek(f.tell()-1)

    return (count - 1)

def go_right_and_count_words(f, until):
    """Returns the distance in words."""
    count = 0
    c = f.read(1)
    while c != "" and f.tell() < until:
        if c == " " or c == "\n":
            count += 1
        c = f.read(1)

    return (count - 1)
