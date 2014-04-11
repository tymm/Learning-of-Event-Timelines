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
from sklearn.metrics import f1_score
from temporalrelation import TemporalRelation

TEXTDIR = "McIntyreLapata09Resources/fables/"

def load_data(new=False, temporal_rel=None, annotations="union", features=["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"], distance=False):
    """Loads the data from fables-100-temporal-dependency.xml into the dataset and shuffles the dataset.

    When new=False the pos and stem feature will be loaded from a file instead of generating them.
    new should be set to True when settings were changed or code was altered.

    If temporal_rel=None the y values will be in [0,1,2,3] which represent the temporal relation classes.
    If temporal_rel in [0,1,2,3] the y values will be 0 or 1 and represent whether a relation has the temporal relation or not.

    If distance is set to True parse_Features() will also return distance information for the data (needed for evaluation)

    """
    # Load data
    data = parse_XML("fables-100-temporal-dependency.xml", TEXTDIR)

    # Extract features
    if distance:
        X, y, distance_diff = parse_Features(data, new, annotations, features, distance)
    else:
        X, y = parse_Features(data, new, annotations, features, distance)

    # Are we interested in all y values or do we just want one class?
    if temporal_rel in [TemporalRelation.BEFORE, TemporalRelation.INCLUDES, TemporalRelation.IS_INCLUDED, TemporalRelation.NONE]:
        # Set same class to 1 and not the same class to 0
        for i, cat in enumerate(y):
            if cat == temporal_rel:
                y[i] = 1
            else:
                y[i] = 0

    # Shuffle the set
    if distance:
        X, y, distance_diff = random_Set(X, y, distance_diff)
        return (X, y, distance_diff)
    else:
        X, y = random_Set(X, y, None)
        return (X, y)

def get_f1_score(X_, y_, class_id):
    X = list(X_)
    y = list(y_)

    # Adjust y for classification
    for i, cat in enumerate(y):
        if cat == class_id:
            y[i] = 1
        else:
            y[i] = 0

    # Split dataset into training set (80%) and test set (20%)
    X_train, X_test, y_train, y_test = split(X, y)

    # Train the random forest classifier
    rf = RandomForestClassifier(n_jobs=2, n_estimators=100)
    rf.fit(X_train, y_train)

    return f1_score(y_test, rf.predict(X_test))

def split(X, y, distance=None):
    """Splits the dataset into a training and test set (80/20)."""
    len_train = len(X)*80/100
    X_train, X_test = X[:len_train], X[len_train:]
    y_train, y_test = y[:len_train], y[len_train:]

    if distance:
        distance_train, distance_test = distance[:len_train], distance[len_train:]
        return (X_train, X_test, y_train, y_test, distance_train, distance_test)
    else:
        return (X_train, X_test, y_train, y_test)


def random_Set(X, y, distance_diff):
    """Takes X and y and returns shuffled X and y. If distance differences are available they will be shuffled in the same way"""
    indices = np.arange(0, len(y))
    shuffle(indices)

    X_new = []
    for idx in indices:
        X_new.append(X[idx])

    if distance_diff:
        distance_diff_new = []
        for idx in indices:
            distance_diff_new.append(distance_diff[idx])

    if distance_diff:
        return (X_new, y[indices], distance_diff_new)
    else:
        return (X_new, y[indices])


def parse_Features(data, new=False, annotations="union", features=["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"], distance=False):
    """Extracts the features out of the dataset and returns a list of features with the corresponding classes.

    Args:
        data (list): The parsed data from fables-100-temporal-dependency.xml.
        new (bool): With new=True a new calculation of Pos() and Stem() can be enforced. Otherwise it will be loaded from a file.
        annotations (str): Looking on all relations ("union") or at all relations in common between the annotators ("intersected").
        features (list): Determines which features should be activated. Possible values: "pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality".
        distance (bool): If set to True parse_Features() will return distance information for the data (needed for evaluation)

    """
    # Only compute pos and stem if new flag is set
    if "pos" in features or "stem" in features:
        if new or not os.path.isfile("set.p"):
                pos = Pos(data, 6, annotations)
                stem = Stem(data, annotations)
                pickle.dump((pos, stem), open("save.p", "wb"))
        else:
            pos, stem = pickle.load(open("save.p", "rb"))

    if distance:
        distance_diff = []

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

            # Append distance information if needed
            if distance:
                distance_diff.append(f.get_distance_diff())

    if distance:
        return (X, y, distance_diff)
    else:
        return (X, y)
