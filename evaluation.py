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
    x = range(len(data))
    y = data

    if xticks:
        x = np.array(range(len(data)))
        plt.xticks(x, xticks)

    plt.xlabel = xlabel
    plt.ylabel = ylabel
    plt.plot(x, y, "ro")
    plt.savefig(filename)

def learning_rate(k=20, new=False):
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


def different_number_of_trees(start=5, end=1000, steps=20, rerunning=20):
    """How does the accuracy change for different amounts of trees."""
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

    return final_accuracies

def union_vs_intersected_relations():
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

if __name__ == "__main__":
    best_feature()
