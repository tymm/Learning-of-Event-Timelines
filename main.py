from train import *

def get_prediction(temporal_rel, new=True, annotations="union", features=["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"]):
    """This function is suited to test the different options and get a result for them

    Args:
        temporal_rel (TemporalRelation): temporal relation we are interested in.
        new (bool): Load features from file (False) or calculate them new (True)?
        annotations (str): Either "union" or "intersected". All data vs. data which annotators have in common
        features (list): Which features should be used

    """
    X, y = load_data(new, temporal_rel, annotations, features)

    # Split dataset into training set (80%) and test set (20%)
    X_train, X_test, y_train, y_test = split(X, y)

    # Train the random forest classifier
    rf = RandomForestClassifier(n_jobs=2, n_estimators=100)
    rf.fit(X_train, y_train)

    # Print accuracy
    print "Accuracy"
    print rf.score(X_test, y_test)
    print

    print "F1-Score"
    print f1_score(y_test, rf.predict(X_test))
    print

    print "Ground truth"
    print y_test
    print
    print "Predicted"
    print rf.predict(X_test)

if __name__ == "__main__":
    # With 'python main.py --reload' a "fresh parsing" will be enforced
    if (len(sys.argv) >= 2 and sys.argv[1] == "--reload") or not os.path.isfile("save.p"):
        new = True
    else:
        new = False

    print "Information for class 0"
    get_prediction(0)
    print

    """
    print "Information for class 1"
    get_prediction(1)
    print

    print "Information for class 2"
    get_prediction(2)
    print

    print "Information for class 3"
    get_prediction(3)
    print
    """
