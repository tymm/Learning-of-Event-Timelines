from parser import parseXML
from helper import get_wordnet_similarity
from aspect import get_aspect
from nltk.stem.lancaster import LancasterStemmer as Stemmer

TEXTDIR = "McIntyreLapata09Resources/fables"

class Feature:
    stemmer = Stemmer()

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
        r = get_aspect(self.relation.target.sentence)
        if r == "simple":
            return 0
        elif r == "perfect":
            return 1
        elif r == "progressive":
            return 2

    # Returns the aspect (simple, progressive, perfect) of the source event
    def get_aspect_source(self):
        r = get_aspect(self.relation.source.sentence)
        if r == "simple":
            return 0
        elif r == "perfect":
            return 1
        elif r == "progressive":
            return 2

    # Returns the combined aspect (9 different values)
    def get_aspect_combined(self):
        if self.get_aspect_source() == 0 and self.get_aspect_target() == 0:
            return 0
        elif self.get_aspect_source() == 0 and self.get_aspect_target() == 1:
            return 1
        elif self.get_aspect_source() == 0 and self.get_aspect_target() == 2:
            return 2
        elif self.get_aspect_source() == 1 and self.get_aspect_target() == 0:
            return 3
        elif self.get_aspect_source() == 1 and self.get_aspect_target() == 1:
            return 4
        elif self.get_aspect_source() == 1 and self.get_aspect_target() == 2:
            return 5
        elif self.get_aspect_source() == 2 and self.get_aspect_target() == 0:
            return 6
        elif self.get_aspect_source() == 2 and self.get_aspect_target() == 1:
            return 7
        elif self.get_aspect_source() == 2 and self.get_aspect_target() == 2:
            return 8
        else:
            return None

    # Returns a number which represents the polarity in the relation
    def get_polarity(self):
        pass

    # Returns a number which gives information about the frequency the event appears in the features time category
    # word of bags
    def get_event_category_source(self):
        pass

    def get_event_category_target(self):
        pass

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

if __name__ == "__main__":
    data = parseXML("training.xml")

    for txt in data.textfiles:
        txt.compute_union_relations()
        for rel in txt.relations_union:
            f = Feature(rel)
            print f.get_distance(), f.get_category()
