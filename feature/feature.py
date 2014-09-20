from preprocessing.word_similarity import get_wordnet_similarity
from preprocessing.aspect import get_aspect
from preprocessing.tense import get_tense
from preprocessing.distance import get_distance as distance
from nltk.stem.lancaster import LancasterStemmer as Stemmer
from nltk import pos_tag, word_tokenize
from sklearn.preprocessing import OneHotEncoder

# Directory to the text data
TEXTDIR = "McIntyreLapata09Resources/fables"

class Feature:

    """Instances of this class are used to extract feature values."""

    stemmer = Stemmer()
    enc_tense = OneHotEncoder(n_values=4, categorical_features=[0,1])
    enc_tense.fit([3, 3])

    enc_aspect = OneHotEncoder(n_values=4, categorical_features=[0,1])
    enc_aspect.fit([3, 3])

    enc_distance = OneHotEncoder(n_values=6, categorical_features=[0])
    enc_distance.fit([5])

    def __init__(self, relation):
        """Constructor of the Feature class.

        Args:
            relation (Relation): Reference to the Relation object we extract the features from.

        """
        self.relation = relation


    def get_distance(self):
        """Returns the number of words between two events in a text as a feature."""
        # We want to compare different objects
        if self.relation.source == self.relation.target:
            return self.enc_distance.transform([[5]]).toarray()[0]
        # The two events have to be in the same file
        if self.relation.source.parent.parent != self.relation.target.parent.parent:
            return self.enc_distance.transform([[5]]).toarray()[0]

        event_distance = distance(self.relation.source.begin, self.relation.target.begin, self.relation.parent.parent.name, TEXTDIR)

        if event_distance < 5:
            return self.enc_distance.transform([[0]]).toarray()[0]
        elif event_distance < 10:
            return self.enc_distance.transform([[1]]).toarray()[0]
        elif event_distance < 15:
            return self.enc_distance.transform([[2]]).toarray()[0]
        elif event_distance < 25:
            return self.enc_distance.transform([[3]]).toarray()[0]
        else:
            return self.enc_distance.transform([[4]]).toarray()[0]

    def get_distance_diff(self):
        """Returns the number of words between two events in a text."""
        # We want to compare different objects
        if self.relation.source == self.relation.target:
            return 0
        # The two events have to be in the same file
        if self.relation.source.parent.parent != self.relation.target.parent.parent:
            return 0

        event_distance = distance(self.relation.source.begin, self.relation.target.begin, self.relation.parent.parent.name, TEXTDIR)
        return event_distance

    def get_similarity_of_words(self):
        """Returns the similarity of two words."""
        # Returns float value
        return get_wordnet_similarity(self.relation.source.content, self.relation.target.content)

    def get_stem_source(self):
        """Returns the word stems of the source event."""
        return self.stemmer.stem(self.relation.source.content)

    def get_stem_target(self):
        """Returns the word stem of the target event."""
        return self.stemmer.stem(self.relation.target.content)

    def get_aspect_target(self):
        """Returns the aspect (simple, progressive, perfect) of the target event."""
        r = get_aspect(self.relation.target.sentence, self.relation.target.content, self.relation.target.num_words_as_event_before_event)
        return r

    def get_aspect_source(self):
        """Returns the aspect (simple, progressive, perfect) of the source event."""
        r = get_aspect(self.relation.source.sentence, self.relation.source.content, self.relation.source.num_words_as_event_before_event)
        return r

    def get_aspect(self):
        """Returns the aspect feature."""
        return self.enc_aspect.transform([[self.get_aspect_source(), self.get_aspect_target()]]).toarray()[0]

    def get_tense_source(self):
        """Returns tense of source event."""
        r = get_tense(self.relation.source.sentence, self.relation.source.content, self.relation.source.num_words_as_event_before_event)
        return r

    def get_tense_target(self):
        """Returns tense of target event."""
        r = get_tense(self.relation.target.sentence, self.relation.target.content, self.relation.target.num_words_as_event_before_event)
        return r

    def get_tense(self):
        """Returns the combined tense."""
        return self.enc_tense.transform([[self.get_tense_source(), self.get_tense_target()]]).toarray()[0]

    def get_polarity(self):
        """Returns a number which represents the polarity in the relation."""
        pol_source = self.relation.source.polarity
        pol_target = self.relation.target.polarity

        if pol_source == 0 and pol_target == 0:
            return 0
        elif pol_source == 1 and pol_target == 0:
            return 1
        elif pol_source == 0 and pol_target == 1:
            return 2
        elif pol_source == 1 and pol_target == 1:
            return 3

    def get_modality(self):
        """Returns a number which represents the modality in the relation."""
        mod_source = self.relation.source.modality
        mod_target = self.relation.target.modality

        if mod_source == 0 and mod_target == 0:
            return 0
        elif mod_source == 1 and mod_target == 0:
            return 1
        elif mod_source == 0 and mod_target == 1:
            return 2
        elif mod_source == 1 and mod_target == 1:
            return 3

    def get_pos_source(self):
        """Returns the part-of-speech tags in an area around the source event defined by Event.pos_surrounding."""
        tags_tokens = pos_tag(word_tokenize(self.relation.source.pos_surrounding))
        tags = [tag[1] for tag in tags_tokens]

        return tags

    def get_pos_target(self):
        """Returns the part-of-speech tags in an area around the target event defined by Event.pos_surrounding."""
        tags_tokens = pos_tag(word_tokenize(self.relation.target.pos_surrounding))
        tags = [tag[1] for tag in tags_tokens]

        return tags

    def get_class(self):
        """Returns number which represents the time relation type."""
        # We only want before, contains and is_contained_in
        return self.relation.temporal_rel

    def get_result(self, category):
        """Returns 1 if the feature is in the category we want and 0 otherwise."""
        if self.relation.time_type == category:
            return 1
        else:
            return 0
