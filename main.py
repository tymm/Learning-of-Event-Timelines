from train import *

def estimate(X_, y_, class_id):
    X = list(X_)
    y = list(y_)

    # Adjust y for classification
    n = 0
    for i, cat in enumerate(y):
        if cat == class_id:
            y[i] = 1
            n += 1
        else:
            y[i] = 0
    print n

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

    if class_id == 3 or class_id == 2:
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

    print "Loading"
    # Load the data which is needed to train the classifier.
    X, y = load_data(new, "union", features=["tense", "aspect"])
    print "Done loading"

    # Information on class 0
    print "Information for class 2"
    estimate(X, y, 2)

    """
    print
    # Information on class 1
    print "Information for class 1"
    estimate(X, y, 1)

    print
    # Information on class 2
    print "Information for class 2"
    estimate(X, y, 2)

    print
    # Information on class 3
    print "Information for class 3"
    estimate(X, y, 3)
    """

