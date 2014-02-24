from train import parse_Features
from parser import parse_XML
import os.path
import cPickle as pickle
import numpy as np
from random import shuffle
from sklearn.ensemble import RandomForestClassifier

def random_Set(X, y, new=False):
    """Takes X and y and returns shuffled X and y.

    If argument new is True, it will shuffle X and y in a new way.
    Otherwise it will load the order of the last time.

    """
    if new == False and os.path.isfile("random_set.p"):
        return pickle.load(open("random_set.p", "rb"))
    else:
        indices = np.arange(0, len(y))
        shuffle(indices)

        X_new = []
        for idx in indices:
            X_new.append(X[idx])

        pickle.dump((X_new, y[indices]), open("random_set.p", "wb"))

        return (X_new, y[indices])


def learning_rate(k=20, new=False):
    if new == False and os.path.isfile("set.p"):
        X, y = pickle.load(open("set.p", "rb"))
    else:
        data = parse_XML("fables-100-temporal-dependency.xml", "McIntyreLapata09Resources/fables/")
        X, y = parse_Features(data)

        pickle.dump((X, y), open("set.p", "wb"))

    # Shuffle the set
    X, y = random_Set(X, y)

    # Split into training and test set (80/20)
    len_train = len(X)*80/100
    X_train, X_test = X[:len_train], X[len_train:]
    y_train, y_test = y[:len_train], y[len_train:]

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

if __name__ == "__main__":
    print learning_rate()
