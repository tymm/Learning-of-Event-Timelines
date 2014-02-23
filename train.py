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

# Create numpy array with samples and targets
data = parse_XML("fables-100-temporal-dependency.xml", "McIntyreLapata09Resources/fables/")

# Since running Pos() and Stem() takes time, load it from a file if present
# With --reload as an argument a new calculation of Pos() and Stem() can be enforced
print "Loading Features"
if (len(sys.argv) >= 2 and sys.argv[1] == "--reload") or not os.path.isfile("save.p"):
    pos = Pos(data, 6)
    stem = Stem(data)
    pickle.dump((pos, stem), open("save.p", "wb"))
else:
    pos, stem = pickle.load(open("save.p", "rb"))

print "Done loading Features"

def parse_Features(data):
    X = []
    y = np.array([], dtype=int)

    null = 0
    for txt in data.textfiles:
        # Use union relations
        txt.compute_union_relations()
        for rel in txt.relations_union:
            f = Feature(rel)
            # If the time relation is not in (before, contains, is_contained_in), skip
            if f.get_category() == -1:
                continue
            if f.get_category() == 0:
                null += 1
            if null > 450:
                continue

            # Make POS feature
            pos_feature = pos.transform(f.get_pos_target(), f.get_pos_source())
            pos_feature = pos_feature.toarray()[0]

            # Make Stem feature
            stem_feature = stem.transform(f.get_stem_source(), f.get_stem_target())
            stem_feature = stem_feature[0]

            # Building a row of all feature values
            feature = [f.get_distance(), f.get_similarity_of_words(), f.get_polarity(), f.get_modality()]
            feature = np.concatenate((feature, f.get_aspect()))
            feature = np.concatenate((feature, pos_feature))
            feature = np.concatenate((feature, stem_feature))
            feature = np.concatenate((feature, f.get_tense()))

            # Append feature to X
            X.append(feature)
            y = np.append(y, [f.get_category()])

    return (X, y)

X, y = parse_Features(data)

# Split dataset in training set(80%) and test set (20%)
len_train = len(X)*80/100
X_train, X_test = X[:len_train], X[len_train:]
y_train, y_test = y[:len_train], y[len_train:]

# Train the random forest classifier
rf = RandomForestClassifier(n_jobs=2, n_estimators=100)
rf.fit(X_train, y_train)

# Print accuracy
print rf.score(X_test, y_test)
print "Predicted:"
print rf.predict(X_test)
print "True values:"
print y_test
