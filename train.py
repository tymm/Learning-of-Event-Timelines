from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from feature.feature import Feature
from parser import parse_XML
from feature.preprocessing.pos import Pos
from feature.preprocessing.stem import Stem
import sys
import cPickle as pickle
import os.path
from random import shuffle

TEXTDIR = "McIntyreLapata09Resources/fables/"

def load_data(new=False, annotations="union", features=["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"]):
    """Loads the data from fables-100-temporal-dependency.xml into the dataset and shuffles the dataset.

    When new=False the dataset and the pos and stem feature will be loaded from a file instead of generating them.
    new should be set to True when settings were changed or code was altered.

    """
    # Load data
    data = parse_XML("fables-100-temporal-dependency.xml", TEXTDIR)

    # Extract features
    X, y = parse_Features(data, new, annotations, features)

    # Shuffle the set
    X, y = random_Set(X, y)
    return (X, y)


def split(X, y):
    """Splits the dataset into a training and test set (80/20)."""
    len_train = len(X)*80/100
    X_train, X_test = X[:len_train], X[len_train:]
    y_train, y_test = y[:len_train], y[len_train:]

    return (X_train, X_test, y_train, y_test)


def random_Set(X, y):
    """Takes X and y and returns shuffled X and y.

    If argument new is True, it will shuffle X and y in a new way.
    Otherwise it will load the order of the last time.

    """
    indices = np.arange(0, len(y))
    shuffle(indices)

    X_new = []
    for idx in indices:
        X_new.append(X[idx])

    return (X_new, y[indices])


def parse_Features(data, new=False, annotations="union", features=["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"]):
    """Extracts the features out of the dataset and returns a list of features with the corresponding classes.

    Args:
        data (list): The parsed data from fables-100-temporal-dependency.xml.
        new (bool): With new=True a new calculation of Pos() and Stem() can be enforced. Otherwise it will be loaded from a file.
        annotations (str): Looking on all relations ("union") or at all relations in common between the annotators ("intersected").
        features (list): Determines which features should be activated. Possible values: "pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality".

    """
    # Only compute pos and stem if new flag is set
    if "pos" in features and "stem" in features:
        if new or not os.path.isfile("set.p"):
                pos = Pos(data, 6, annotations)
                stem = Stem(data, annotations)
                pickle.dump((pos, stem), open("save.p", "wb"))
        else:
            pos, stem = pickle.load(open("save.p", "rb"))

    X = []
    y = np.array([], dtype=int)

    for txt in data.textfiles:
        # Union or intersected relations?
        if annotations == "union":
            txt.compute_union_relations()
        elif annotations == "intersected":
            txt.compute_intersection_relations()

        for rel in txt.relations:
            f = Feature(rel)

            feature = []

            # Make polarity feature
            if "polarity" in features:
                feature = np.concatenate((feature, [f.get_polarity()]))

            # Make distance feature
            if "distance" in features:
                feature = np.concatenate((feature, f.get_distance()))

            # Make POS feature
            if "pos" in features:
                pos_feature = pos.transform(f.get_pos_target(), f.get_pos_source())
                pos_feature = pos_feature.toarray()[0]
                feature = np.concatenate((feature, pos_feature))

            # Make Stem feature
            if "stem" in features:
                stem_feature = stem.transform(f.get_stem_source(), f.get_stem_target())
                stem_feature = stem_feature[0]
                feature = np.concatenate((feature, stem_feature))

            # Make similarity feature
            if "similarity" in features:
                feature = np.concatenate((feature, [f.get_similarity_of_words()]))

            # Make modality feature
            if "modality" in features:
                feature = np.concatenate((feature, [f.get_modality()]))

            # Make aspect feature
            if "aspect" in features:
                feature = np.concatenate((feature, f.get_aspect()))

            # Make tense feature
            if "tense" in features:
                feature = np.concatenate((feature, f.get_tense()))

            # Append feature to X
            X.append(feature)
            y = np.append(y, [f.get_class()])

    return (X, y)
