from parsexml.text_structure import Text_structure
from parsexml.relation import Relation

class Annotator():

    """Instances of this class are used to describe an annotator from fables-100-temporal-dependency.xml. It is mainly used to distinguish between union and intersecting events or relations."""

    def __init__(self, id_=None, parent=None, xml_id=None):
        """Constructor of the Annotator class

        Args:
            id_ (int): Unique id (not needed so far).
            parent (Text): Reference to the corresponding Text object.
            xml_id (str): Id used in fables-100-temporal-dependency.xml.

        Attributes:
            events (list): All events annotated by an annotator
            relations (list): All relations annotated by an annotator

        """
        self.parent = parent
        self.events = []
        self.relations = []
        self.id_ = id_
        self.xml_id = xml_id
        self.text_structure = None

    def remove_none_relations(self):
        """Removes relations which are not "before", "includes" or "is_included"."""
        relations_without_none = []
        for relation in self.relations:
            if relation.temporal_rel is not None:
                relations_without_none.append(relation)

        self.relations = relations_without_none

    def create_other_relations(self):
        """Create relations (with NONE-relation if not existing already) between all events in the same sentence and between main-events of consecutive sentences."""
        other_relations = []

        for e1 in self.events:
            for e2 in self.events:
                if not self._are_events_in_a_relation(e1, e2):
                    if self._are_events_in_same_sentence(e1, e2) or self._are_events_in_consecutive_sentences(e1, e2):
                        # Create NONE-relation between events
                        rel = Relation(self, e1, e2, "none")
                        other_relations.append(rel)

        self.relations += other_relations


    def _are_events_in_a_relation(self, source, target):
        for relation in self.relations:
            if relation.source == source and relation.target == target:
                return True
        else:
            False

    def _are_events_in_same_sentence(self, e1, e2):
        structure = self.text_structure.structure

        for sentence in self.text_structure.sentences:
            if e1 in structure[sentence] and e2 in structure[sentence]:
                return True
        else:
            return False

    def _are_events_in_consecutive_sentences(self, e1, e2):
        structure = self.text_structure.structure

        # Find sentence of e1
        sentence_e1 = None
        for sentence in self.text_structure.sentences:
            if e1 in structure[sentence]:
                sentence_e1 = sentence
                break

        index_e1 = self.text_structure.sentences.index(sentence_e1)

        # Find sentence of e2
        sentence_e2 = None
        for sentence in self.text_structure.sentences:
            if e2 in structure[sentence]:
                sentence_e2 = sentence
                break

        if sentence_e2 is None:
            print e2.content
            print e2.sentence
            print e2.parent.parent.name

        index_e2 = self.text_structure.sentences.index(sentence_e2)

        if abs(index_e1-index_e2) == 1:
            return True
        else:
            return False

    def create_text_structure(self):
        self.text_structure = Text_structure(self)
