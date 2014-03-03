from train import parse_Features
from train import load_data
from train import split
from train import random_Set
from parser import parse_XML
import os.path
import cPickle as pickle
import numpy as np
from random import shuffle
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

def plot(filename, xlabel, ylabel, data, xticks=None):
    """Ploting data to file.

    If xticks is not None and a list of values, they will be used to label the x-axis.

    """
    x = range(len(data))
    y = data

    if xticks:
        x = np.array(range(len(data)))
        plt.xticks(x, xticks, size="small")

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(x, y, "ro")
    plt.savefig(filename)

def learning_rate(k=20, new=False):
    """Splits the dataset into k pieces and builds a series out of those k pieces. For every partial sum the accuracy will be calculated to obtain the learning rate."""
    X, y = load_data(new)

    X_train, X_test, y_train, y_test = split(X, y)

    # Splitting the training set up into k pieces
    len_piece = len(X_train)/k
    X_pieces = []
    y_pieces = []

    for i in range(k):
        offset = i*len_piece

        X_piece = X[offset:][:len_piece]
        y_piece = y[offset:][:len_piece]

        X_pieces.append(X_piece)
        y_pieces.append(y_piece)

    # Building series (from 0 to k) for those pieces
    X_series = []
    y_series = []

    for i in range(k):
        X_sum = X_pieces[0]
        y_sum = y_pieces[0]
        for j in range(i):
            X_sum = np.concatenate((X_sum, X_pieces[j]))
            y_sum = np.concatenate((y_sum, y_pieces[j]))

        X_series.append(X_sum)
        y_series.append(y_sum)

    # Calculate the accuracy for each partial sum
    rf = RandomForestClassifier(n_jobs=2, n_estimators=1000)
    accuracies = []

    for partial_X, partial_y in zip(X_series, y_series):
        rf.fit(partial_X, partial_y)
        accuracies.append(rf.score(X_test, y_test))

    return accuracies


def different_number_of_trees(start=5, end=1000, steps=20, rerunning=15):
    """How does the accuracy change for different amounts of trees. Plots that to different_number_of_trees.jpg"""
    X, y = load_data()
    X_train, X_test, y_train, y_test = split(X, y)

    # Since accuracies for small amounts of trees differ a lot, we take the average over many tries
    many_accuracies = []
    for x in range(rerunning):
        accuracies = []
        for i in range(start, end, steps):
            rf = RandomForestClassifier(n_jobs=2, n_estimators=i)
            rf.fit(X_train, y_train)
            accuracies.append(rf.score(X_test, y_test))

        many_accuracies.append(accuracies)

    final_accuracies = []
    # Calculate the mean
    for i in range(len(many_accuracies[0])):
        mean = []
        for j in range(len(many_accuracies)):
            mean.append(many_accuracies[j][i])
        final_accuracies.append(np.mean(mean))

    plot("different_number_of_trees.jpg", "accuracy", "trees", final_accuracies)

def union_vs_intersected_relations():
    """Looking at the difference in accuracy when all relations (union) are used vs. all events are used which the annotators have in common (intersected)."""
    X_union, y_union = load_data(new=True, annotations="union")
    X_intersected, y_intersected = load_data(new=True, annotations="intersected")

    X_u_train, X_u_test, y_u_train, y_u_test = split(X_union, y_union)
    X_i_train, X_i_test, y_i_train, y_i_test = split(X_intersected, y_intersected)

    rf_u = RandomForestClassifier(n_jobs=2, n_estimators=100)
    rf_u.fit(X_u_train, y_u_train)

    rf_i = RandomForestClassifier(n_jobs=2, n_estimators=100)
    rf_i.fit(X_i_train, y_i_train)

    print "Union: " + str(rf_u.score(X_u_test, y_u_test))
    print "Intersected: " + str(rf_i.score(X_i_test, y_i_test))


def best_feature():
    """Look at the accuracies for all features in isolation."""
    features = ["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"]

    data = parse_XML("fables-100-temporal-dependency.xml", "McIntyreLapata09Resources/fables/")

    accuracies = []

    for feature in features:
        X, y = parse_Features(data, new=True, annotations="union", features=[feature])

        X, y = random_Set(X, y)

        X_train, X_test, y_train, y_test = split(X, y)

        rf = RandomForestClassifier(n_jobs=2, n_estimators=100)
        rf.fit(X_train, y_train)
        accuracies.append({feature : rf.score(X_test, y_test)})

    data = [x.values()[0] for x in accuracies]

    plot("best_features.jpg", "x", "y", data, features)

def get_distance_data(data):
    """Extracts the distance feature into the following data structure which will be returned: [{distance : classified_right?}, ...]"""
    X, y = load_data(new=True)
    X_train, X_test, y_train, y_test = split(X, y)

    rf = RandomForestClassifier(n_jobs=2, n_estimators=100)
    rf.fit(X_train, y_train)

    # The distance value is at postition 0 if it is enabled
    distance = [x[0] for x in X_test]

    predicted_y = rf.predict(X_test)

    # Make array with elements like this {distance : predicted_right?}
    for i in range(len(X_test)):
        if y_test[i] == predicted_y[i]:
            data.append({X_test[i][0] : True})
        else:
            data.append({X_test[i][0] : False})

    return data

def distance_importance():
    """Returns distance_importance.jpg which describes how the accuracy changes when looking at the distance between events which are related."""
    # Get enough data on the distance
    data = []
    for i in range(3):
        get_distance_data(data)

    # Divide space of possible distances into parts of same size
    # datastructure: [{part: [start_distance, end_distance, num_true_positive, num_false_positive]}, ...]
    parts = [{1: [0, 20, 0, 0]}, {2: [21, 40, 0, 0]}, {3: [41, 60, 0, 0]}, {4: [61, 80, 0, 0]}, {5: [81, 100, 0, 0]}, {6: [101, 120, 0, 0]}, {7: [121, 140, 0, 0]}, {8: [141, 160, 0, 0]}, {9: [161, 180, 0, 0]}, {10: [181, 200, 0, 0]}, {11: [201, 220, 0, 0]}, {12: [221, 240, 0, 0]}, {13: [241, 260, 0, 0]}, {14: [261, 280, 0, 0]}, {15: [281, 300, 0, 0]}]

    # Put distribution of false positives and true positives into parts
    for d in data:
        for p in parts:
            distance = d.keys()[0]
            start_distance = p.values()[0][0]
            end_distance = p.values()[0][1]
            if distance >= start_distance and distance <= end_distance:
                predicted = d.values()[0]
                key = p.keys()[0]
                value = p.values()[0]
                # True positive
                if predicted:
                    value[2] += 1
                    p.update({key: value})
                # False positive
                else:
                    value[3] += 1
                    p.update({key: value})

    # Calculating the ratio between true and false positives
    ratios = []
    for p in parts:
        true_positives = p.values()[0][2]
        false_positives = p.values()[0][3]
        try:
            ratio = true_positives/float(false_positives)
            ratios.append(ratio)
        except ZeroDivisionError:
            ratios.append(true_positives)


    plot("distance_importance.jpg", "distance in characters", "ratio: true_positives/false_postives", ratios, ["0-20", "21-40", "41-60", "61-80", "81-100", "101-120", "121-140", "141-160", "161-180", "181-200", "201-220", "221-240", "241-260", "261-280", "281-300"])

if __name__ == "__main__":
    different_number_of_trees()
