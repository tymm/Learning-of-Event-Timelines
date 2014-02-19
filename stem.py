import numpy as np
from sklearn.preprocessing import OneHotEncoder
from extract_features import Feature

class Stem():
    def __init__(self, data):
        # OneHotEncoder to encode categorical integer features
        self.encoder = OneHotEncoder()

        # All unique stems
        self.stems = self.load_stems(data)

        # Number of different stems
        self.count = len(self.stems)

        # Fit the encoder
        self.encoder_fit()

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
        return np.where(self.stems==stem)[0][0]

    def encoder_fit(self):
        # Small hack to simulate the input matrix of integers for the encoder
        different_values = range(self.count)
        splitted = []
        for val in different_values:
            splitted.append([val])
        self.encoder.fit(splitted)

    # Turn stems into binary feature
    def transform(self, stem_source, stem_target):
        integer_source = self.stem_to_integer(stem_source)
        integer_target = self.stem_to_integer(stem_target)

        binary_source = self.encoder.transform([[integer_source]])
        binary_target = self.encoder.transform([[integer_target]])

        # Concatenate and return
        return np.concatenate((binary_source.toarray(), binary_target.toarray()))

