import numpy as np
from sklearn.preprocessing import OneHotEncoder
from feature.feature import Feature

class Stem():
    def __init__(self, data):
        # All unique stems
        self.stems = self.load_stems(data)

        # Number of different stems
        self.count = len(self.stems)

        # OneHotEncoder to encode categorical integer features
        self.encoder = OneHotEncoder(n_values=self.count, categorical_features=[0])
        self.encoder.fit([self.count-1])

    def load_stems(self, data):
        # Get all word stems
        stems = np.array([])
        for txt in data.textfiles:
            # Use union relations
            txt.compute_union_relations()
            for rel in txt.relations_union:
                f = Feature(rel)
                if f.get_category() == -1:
                    continue
                stems = np.append(stems, [f.get_stem_target()])
                stems = np.append(stems, [f.get_stem_source()])

        stems = np.unique(stems)
        return stems

    # Translates stem to integer
    def stem_to_integer(self, stem):
        try:
            return np.where(self.stems==stem)[0][0]
        except IndexError:
            print self.stems

    # Turn stems into binary feature
    def transform(self, stem_source, stem_target):
        integer_source = self.stem_to_integer(stem_source)
        integer_target = self.stem_to_integer(stem_target)

        binary_source = self.encoder.transform([[integer_source]])
        binary_target = self.encoder.transform([[integer_target]])

        # Concatenate and return
        return np.concatenate((binary_source.toarray(), binary_target.toarray()))

