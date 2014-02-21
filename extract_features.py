from helper import get_wordnet_similarity
from aspect import get_aspect
from tense import get_tense
from nltk.stem.lancaster import LancasterStemmer as Stemmer
from nltk import pos_tag, word_tokenize
from sklearn.preprocessing import OneHotEncoder

TEXTDIR = "McIntyreLapata09Resources/fables"

class Feature:
    stemmer = Stemmer()
    enc_tense = OneHotEncoder(n_values=10, categorical_features=[0,1])
    enc_tense.fit([9, 9])

    def __init__(self, relation):
        self.relation = relation


    # Returns the number of characters between two events in a text
    def get_distance(self):
        # We want to compare different objects
        if self.relation.source == self.relation.target:
            return False
        # The two events have to be in the same file
        if self.relation.source.parent.parent != self.relation.target.parent.parent:
            return False

        # Distance is measured in characters between the end of the first word and the beginning of the second word
        if self.relation.source.begin > self.relation.target.begin:
            return (self.relation.source.begin - self.relation.target.end)
        elif self.relation.source.begin < self.relation.target.begin:
            return (self.relation.target.begin - self.relation.source.end)

    # Returns the similarity of two words
    def get_similarity_of_words(self):
        # Returns float value
        return get_wordnet_similarity(self.relation.source.content, self.relation.target.content)

    # Returns the word stems of the source event
    def get_stem_source(self):
        return self.stemmer.stem(self.relation.source.content)

    # Returns the word stem of the target event
    def get_stem_target(self):
        return self.stemmer.stem(self.relation.target.content)

    # Returns the aspect (simple, progressive, perfect) of the target event
    def get_aspect_target(self):
        r = get_aspect(self.relation.target.surrounding)
        if r == "simple":
            return 0
        elif r == "perfect":
            return 1
        elif r == "progressive":
            return 2

    # Returns the aspect (simple, progressive, perfect) of the source event
    def get_aspect_source(self):
        r = get_aspect(self.relation.source.surrounding)
        if r == "simple":
            return 0
        elif r == "perfect":
            return 1
        elif r == "progressive":
            return 2

    # Returns the aspect feature (9 different values)
    def get_aspect(self):
        if self.get_aspect_source() == 0 and self.get_aspect_target() == 0:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif self.get_aspect_source() == 0 and self.get_aspect_target() == 1:
            return [1, 0, 0, 0, 0, 0, 0, 0, 0]
        elif self.get_aspect_source() == 0 and self.get_aspect_target() == 2:
            return [0, 1, 0, 0, 0, 0, 0, 0, 0]
        elif self.get_aspect_source() == 1 and self.get_aspect_target() == 0:
            return [0, 0, 1, 0, 0, 0, 0, 0, 0]
        elif self.get_aspect_source() == 1 and self.get_aspect_target() == 1:
            return [0, 0, 0, 1, 0, 0, 0, 0, 0]
        elif self.get_aspect_source() == 1 and self.get_aspect_target() == 2:
            return [0, 0, 0, 0, 1, 0, 0, 0, 0]
        elif self.get_aspect_source() == 2 and self.get_aspect_target() == 0:
            return [0, 0, 0, 0, 0, 1, 0, 0, 0]
        elif self.get_aspect_source() == 2 and self.get_aspect_target() == 1:
            return [0, 0, 0, 0, 0, 0, 1, 0, 0]
        elif self.get_aspect_source() == 2 and self.get_aspect_target() == 2:
            return [0, 0, 0, 0, 0, 0, 0, 1, 0]
        else:
            return [0, 0, 0, 0, 0, 0, 0, 0, 1]

    # Returns tense of source event
    def get_tense_source(self):
        r = get_tense(self.relation.source.surrounding)
        return r

    # Returns tense of target event
    def get_tense_target(self):
        r = get_tense(self.relation.target.surrounding)
        return r

    # Returns the combined tense
    def get_tense(self):
        return self.enc_tense.transform([[self.get_tense_source(), self.get_tense_target()]]).toarray()[0]

    # Returns a number which represents the polarity in the relation
    def get_polarity(self):
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

    # Returns a number which represents the modality in the relation
    def get_modality(self):
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
        tags_tokens = pos_tag(word_tokenize(self.relation.source.pos_surrounding))
        tags = [tag[1] for tag in tags_tokens]

        return tags

    def get_pos_target(self):
        tags_tokens = pos_tag(word_tokenize(self.relation.target.pos_surrounding))
        tags = [tag[1] for tag in tags_tokens]

        return tags

    # Returns number which represents the time relation type
    def get_category(self):
        # We only want before, contains and is_contained_in
        if self.relation.time_type == "before":
            return 0
        elif self.relation.time_type == "includes":
            return 1
        elif self.relation.time_type == "is_included":
            return 2
        else:
            return -1

    # Returns 1 if the feature is in the category we want and 0 otherwise
    def get_result(self, category):
        if self.relation.time_type == category:
            return 1
        else:
            return 0
