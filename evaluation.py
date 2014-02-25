from train import parse_Features
from train import load_data
from parser import parse_XML
import os.path
import cPickle as pickle
import numpy as np
from random import shuffle
from sklearn.ensemble import RandomForestClassifier


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


def different_number_of_trees(start=5, end=1000, steps=20):
    """How does the accuracy change for different amounts of trees."""
    X, y = load_data()
    X_train, X_test, y_train, y_test = split(X, y)

    # Since accuracies for small amounts of trees differ a lot, we take the average over many trys
    many_accuracies = []
    for x in range(100):
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


if __name__ == "__main__":
    print different_number_of_trees()
