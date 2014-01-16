from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from extract_features import Feature
from parser import parseXML
import pandas as pd

def split(indices):
    """ split indices into two parts: 80%, 20% """
    size = indices.shape[0]
    x = size * 0.8
    return indices[:x], indices[x:]

# Create numpy array with samples and targets
data = parseXML("fables-100-temporal-dependency.xml")

X = np.array([])
y = np.array([])

for txt in data.textfiles:
    # Use union relations
    txt.compute_union_relations()
    for rel in txt.relations_union:
        f = Feature(rel)
        # If the time relation is not in (before, contains, is_contained_in), skip
        if f.get_category() == -1:
            continue
        X = np.append(X, [f.get_distance()])
        y = np.append(y, [f.get_category()])

print X.shape
print y.shape

df_samples = pd.DataFrame(X, columns=['distance between events'])

# split dataset in training and test set
len_train = len(df_samples)*80/100
df_train, df_test = df_samples[:len_train], df_samples[len_train:]
y_train, y_test = y[:len_train], y[len_train:]


# train classifier
rf = RandomForestClassifier(n_estimators=1000)
rf.fit(df_train, y)

# print accuracy
print rf.score(df_test, y)
