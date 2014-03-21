import numpy as np
from sklearn.preprocessing import OneHotEncoder
from feature.feature import Feature

class Stem():
    def __init__(self, data, annotations):
        """Constructor of the Stem class.

        Args:
            data (list): Parsed xml information from parser.parse_XML().
            number_tags_per_feature (int): Number of tags per feature.
            annotations (str): Looking on all relations ("union") or at all relations in common between the annotators ("intersected").

        """
        # Union or intersected relations?
        self.annotations = annotations

        # All unique stems
        self.stems = self.load_stems(data)

        # Number of different stems
        self.count = len(self.stems)

        # OneHotEncoder to encode categorical integer features
        self.encoder = OneHotEncoder(n_values=self.count, categorical_features=[0])
        self.encoder.fit([self.count-1])

    def load_stems(self, data):
        """Returns all word stems used in the parsed XML data."""
        # Get all word stems
        stems = np.array([])
        for txt in data.textfiles:
            if self.annotations == "union":
                txt.compute_union_relations()
            elif self.annotations == "intersected":
                txt.compute_intersection_relations()

            for rel in txt.relations:
                f = Feature(rel)
                stems = np.append(stems, [f.get_stem_target()])
                stems = np.append(stems, [f.get_stem_source()])

        stems = np.unique(stems)
        return stems

    def stem_to_integer(self, stem):
        """Translates a stem to an integer value."""
        try:
            return np.where(self.stems==stem)[0][0]
        except IndexError:
            print self.stems

    def transform(self, stem_source, stem_target):
        """Turn stems into binary feature."""
        integer_source = self.stem_to_integer(stem_source)
        integer_target = self.stem_to_integer(stem_target)

        binary_source = self.encoder.transform([[integer_source]])
        binary_target = self.encoder.transform([[integer_target]])

        # Concatenate and return
        return np.concatenate((binary_source.toarray(), binary_target.toarray()))

