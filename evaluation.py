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
from sklearn.metrics import f1_score, recall_score, precision_score
from temporalrelation import TemporalRelation

def plot(filename, xlabel, ylabel, data, xticks=None):
    """Ploting data to file.

    If xticks is not None and a list of values, they will be used to label the x-axis.

    """
    x = range(len(data))
    y = data

    if xticks:
        x = np.array(range(len(data)))
        plt.xticks(x, xticks, size="xx-small", rotation="vertical")

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.plot(x, y, "ro")
    plt.savefig(filename)

def learning_rate(temporal_rel, k=20, new=False):
    """Splits the dataset into k pieces and builds a series out of those k pieces. For every partial sum the accuracy will be calculated to obtain the learning rate. Plots the data to learning_rate.jpg"""
    X, y = load_data(new, temporal_rel)

    X_train, X_test, y_train, y_test = split(X, y)

    # Splitting the training set up into k pieces
    len_piece = len(X_train)/k
    X_pieces = []
    y_pieces = []
    data_count = []
    recall = []
    precision = []

    for i in range(k):
        data_count.append((i+1)*len_piece)
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
        y_pred = rf.predict(X_test)
        accuracies.append(f1_score(y_test, y_pred))
        recall.append(recall_score(y_test, y_pred))
        precision.append(precision_score(y_test, y_pred))

    if temporal_rel == None:
        plot("learning_rate_weighted.jpg", "data_count", "f1_score", accuracies, data_count)
    else:
        plot("learning_rate_"+str(temporal_rel)+".jpg", "data_count", "f1_score", accuracies, data_count)
    print recall
    print precision


def different_number_of_trees(temporal_rel, start=5, end=800, steps=20, rerunning=5):
    """How does the accuracy change for different amounts of trees. Plots to different_number_of_trees.jpg"""
    X, y = load_data(True, temporal_rel)
    X_train, X_test, y_train, y_test = split(X, y)

    # Since accuracies for small amounts of trees differ a lot, we take the average over many tries
    many_accuracies = []
    many_recall = []
    many_precision = []
    for x in range(rerunning):
        accuracies = []
        recall = []
        precision = []
        for i in range(start, end, steps):
            rf = RandomForestClassifier(n_jobs=2, n_estimators=i)
            rf.fit(X_train, y_train)

            y_pred = rf.predict(X_test)

            accuracies.append(f1_score(y_test, y_pred))
            recall.append(recall_score(y_test, y_pred))
            precision.append(precision_score(y_test, y_pred))

        many_accuracies.append(accuracies)
        many_recall.append(recall)
        many_precision.append(precision)

    final_accuracies = []
    final_recall = []
    final_precision = []
    # Calculate the mean
    for i in range(len(many_accuracies[0])):
        mean = []
        mean_recall = []
        mean_precision = []
        for j in range(len(many_accuracies)):
            mean.append(many_accuracies[j][i])
            mean_recall.append(many_recall[j][i])
            mean_precision.append(many_precision[j][i])
        final_accuracies.append(np.mean(mean))
        final_recall.append(np.mean(mean_recall))
        final_precision.append(np.mean(mean_precision))

    # xticks
    xticks = range(start, end, steps)

    if temporal_rel == None:
        plot("different_number_of_trees_weighted.jpg", "number_of_trees", "f1_score", final_accuracies, xticks)
    else:
        plot("different_number_of_trees_"+str(temporal_rel)+".jpg", "number_of_trees", "f1_score", final_accuracies, xticks)
    print final_recall
    print final_precision

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

    y_u_pred = rf.predict(X_u_test)
    y_i_pred = rf.predict(X_i_test)
    print "Union: " + str(f1_score(y_u_test, y_u_pred))
    print "Intersected: " + str(f1_score(y_i_test, y_i_test))


def best_feature(temporal_rel):
    """Look at the accuracies for all features in isolation."""
    features = ["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"]

    accuracies = []
    recall = []
    precision = []

    for feature in features:
        X, y = load_data(True, temporal_rel, features=[feature])
        X_train, X_test, y_train, y_test = split(X, y)

        rf = RandomForestClassifier(n_jobs=2, n_estimators=100)
        rf.fit(X_train, y_train)

        y_pred = rf.predict(X_test)

        accuracies.append({feature : f1_score(y_test, y_pred)})
        recall.append({feature : recall_score(y_test, y_pred)})
        precision.append({feature : precision_score(y_test, y_pred)})
        print "Done with feature"

    # Add all features
    X, y = load_data(True, temporal_rel)
    X_train, X_test, y_train, y_test = split(X, y)

    rf = RandomForestClassifier(n_jobs=2, n_estimators=100)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    accuracies.append({"all": f1_score(y_test, y_pred)})
    recall.append({"all": recall_score(y_test, y_pred)})
    precision.append({"all": precision_score(y_test, y_pred)})
    features.append("all")


    data = [x.values()[0] for x in accuracies]

    if temporal_rel == None:
        plot("best_feature_weighted.jpg", "feature", "f1_score", data, features)
    else:
        plot("best_feature_"+str(temporal_rel)+".jpg", "feature", "f1_score", data, features)
    print recall
    print precision

def get_distance_data(data, temporal_rel):
    """Extracts the distance feature into the following data structure which will be returned: [{distance : classified_right?}, ...]"""
    X, y, distance = load_data(True, temporal_rel, distance=True)
    X_train, X_test, y_train, y_test, distance_train, distance_test = split(X, y, distance)

    rf = RandomForestClassifier(n_jobs=2, n_estimators=100)
    rf.fit(X_train, y_train)

    y_pred  = rf.predict(X_test)

    # Make array with elements like this {distance : [TruePositive?, TrueNegative?, FalsePositive?, FalseNegative?]}
    for i in range(len(X_test)):
        if y_test[i] == y_pred[i] and y_test[i] == 1:
            # True positive
            data.append({distance_test[i] : [True, False, False, False]})
        elif y_test[i] == y_pred[i] and y_test[i] == 0:
            # True negative
            data.append({distance_test[i] : [False, True, False, False]})
        elif y_test[i] != y_pred[i] and y_pred[i] == 1:
            # False positive
            data.append({distance_test[i] : [False, False, True, False]})
        elif y_test[i] != y_pred[i] and y_pred[i] == 0:
            # False negative
            data.append({distance_test[i] : [False, False, False, True]})


def distance_importance(temporal_rel):
    """Returns distance_importance.jpg which describes how the accuracy changes when looking at the distance between events which are related."""
    # Get enough data on the distance
    data = []
    for i in range(3):
        get_distance_data(data, temporal_rel)

    # Divide space of possible distances into parts of same size
    # datastructure: [{part: [start_distance, end_distance, num_true_positive, num_true_negatives, num_false_positives, num_false_negatives]}, ...]
    parts = [{1: [0, 3, 0, 0, 0, 0]}, {2: [4, 7, 0, 0, 0, 0]}, {3: [8, 11, 0, 0, 0, 0]}, {4: [12, 15, 0, 0, 0, 0]}, {5: [16, 19, 0, 0, 0, 0]}, {6: [20, 23, 0, 0, 0, 0]}, {7: [24, 27, 0, 0, 0, 0]}, {8: [28, 31, 0, 0, 0, 0]}]

    # Put distribution of TP, TN, FP, FN into parts
    for d in data:
        for p in parts:
            distance = d.keys()[0]
            start_distance = p.values()[0][0]
            end_distance = p.values()[0][1]
            if distance >= start_distance and distance <= end_distance:
                true_pos = d.values()[0][0]
                true_neg = d.values()[0][1]
                false_pos = d.values()[0][2]
                false_neg = d.values()[0][3]

                key = p.keys()[0]
                value = p.values()[0]

                # True positive
                if true_pos:
                    value[2] += 1
                    p.update({key: value})
                # True negative
                elif true_neg:
                    value[3] += 1
                    p.update({key: value})
                # False positiv
                elif false_pos:
                    value[4] += 1
                    p.update({key: value})
                # False negative
                elif false_neg:
                    value[5] += 1
                    p.update({key: value})

    # Calculating the ratio between true and false positives
    f1_scores = []
    for p in parts:
        true_pos = p.values()[0][2]
        true_neg = p.values()[0][3]
        false_pos = p.values()[0][4]
        false_neg = p.values()[0][5]
        try:
            f1_score = (2*true_pos)/float(2*true_pos + false_pos + false_neg)
            f1_scores.append(f1_score)
        except ZeroDivisionError:
            f1_scores.append(0)


    plot("distance_importance_"+str(temporal_rel)+".jpg", "distance in words", "f1-score", f1_scores, ["0-3", "4-7", "8-11", "12-15", "16-19", "20-23", "24-27", "28-31"])

if __name__ == "__main__":
    # Generate learning rate plot
    #learning_rate(None, new=True)

    # Generate best feature plot
    # best_feature(TemporalRelation.NONE)

    # Generate different number of trees plot
    # different_number_of_trees(TemporalRelation.NONE)

    # Generate distance importance plot
    distance_importance(TemporalRelation.NONE)
