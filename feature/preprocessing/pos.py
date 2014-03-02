import numpy as np
from sklearn.preprocessing import OneHotEncoder
from feature.feature import Feature

class Pos():
    def __init__(self, data, number_tags_per_feature, annotations):
        """Constructor of the Pos class.

        Args:
            data (list): Parsed xml information from parser.parse_XML().
            number_tags_per_feature (int): Number of tags per feature.
            annotations (str): Looking on all relations ("union") or at all relations in common between the annotators ("intersected").

        """
        # OneHotEncoder to encode categorical integer features
        self.encoder = OneHotEncoder()

        # At how many POS tags are we looking for one feature (defined in Event class)
        self.number_tags_per_feature = number_tags_per_feature

        # Union or intersected relations?
        self.annotations = annotations

        # All unique tags in text form
        self.pos_tags = self.load_pos_tags(data)

        # All possible features in integer representation
        self.integer_features = self.load_integer_features(data)

        # Fit the encoder with the help of all possible features in integer represenation
        self.encoder_fit()


    def load_pos_tags(self, data):
        """Loads all POS tags used in the pos_surrounding area around an event."""
        pos_tags = np.array([])

        for txt in data.textfiles:
            if self.annotations == "union":
                txt.compute_union_relations()
            elif self.annotations == "intersected":
                txt.compute_intersection_relations()

            for rel in txt.relations:
                f = Feature(rel)
                if f.get_class() == -1:
                    continue
                # Collect all pos tags from the data
                pos_tags = np.concatenate((pos_tags, f.get_pos_target()))
                pos_tags = np.concatenate((pos_tags, f.get_pos_source()))

        pos_tags = np.unique(pos_tags)

        # Append a blank tag which will be used for filling up features which don't have enough elements
        pos_tags = np.append(pos_tags, 'BL')
        return pos_tags

    def load_integer_features(self, data):
        """Gives each POS tag in data a number."""
        integer_features = []
        pos_feature = np.array([])

        for txt in data.textfiles:
            if self.annotations == "union":
                txt.compute_union_relations()
            elif self.annotations == "intersected":
                txt.compute_intersection_relations()

            for rel in txt.relations:
                f = Feature(rel)
                if f.get_class() == -1:
                    continue
                # Build arrays of integers with which we can fit the encoder
                # Standardize because f.get_pos_$x() doesn't have to be of length self.number_tags_per_feature/2
                standardized_pos_target = self.standardize_sub_pos_feature(f.get_pos_target())
                standardized_pos_source = self.standardize_sub_pos_feature(f.get_pos_source())
                # Concatenate the two plain POS tag arrays from target and source event
                pos_feature = np.concatenate((standardized_pos_target, standardized_pos_source))
                # Transform this array into the corresponding array of integers
                integer_feature = self.pos_tags_to_integers(pos_feature)

                integer_features.append(integer_feature)

        return integer_features

    def standardize_sub_pos_feature(self, sub_pos_feature):
        """Standardizes a part of the feature. If it is too long or too short, the length will be adjusted."""
        if len(sub_pos_feature) > (self.number_tags_per_feature/2):
            # Remove something if we have to many POS tags
            diff = len(sub_pos_feature) - (self.number_tags_per_feature/2)
            # First try to remove '``' and if this is not present just remove the first element
            for i in range(diff):
                if '``' in sub_pos_feature:
                    sub_pos_feature.remove('``')
                else:
                    sub_pos_feature.remove(sub_pos_feature[0])

        elif len(sub_pos_feature) < (self.number_tags_per_feature/2):
            # Fill it up with blanks
            diff = (self.number_tags_per_feature/2) - len(sub_pos_feature)
            for i in range(diff):
                sub_pos_feature.append('BL')

        return sub_pos_feature

    def pos_to_integer(self, pos_tag):
        """Translates POS tag to number."""
        return np.where(self.pos_tags==pos_tag)[0][0]

    def pos_tags_to_integers(self, pos_tags):
        """Translates array of POS tags to array of numbers."""
        numbers = []
        for tag in pos_tags:
            numbers.append(self.pos_to_integer(tag))

        return numbers

    def encoder_fit(self):
        """Fit the encoder to all possible pos tags and the dimension of tags to encode."""
        self.encoder.fit(self.integer_features)

    def transform(self, pos_tags_target, pos_tags_source):
        """Turn pos tags into binary feature."""
        # Standardize input features
        standardized_pos_target = self.standardize_sub_pos_feature(pos_tags_target)
        standardized_pos_source = self.standardize_sub_pos_feature(pos_tags_source)
        # Concatenate both arrays
        integers = self.pos_tags_to_integers(np.concatenate((standardized_pos_target, standardized_pos_source)))
        return self.encoder.transform([integers])
