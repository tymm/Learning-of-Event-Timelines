from lxml import etree
from copy import deepcopy
from helper import get_sentence, get_surrounding
from polarity import get_polarity
from modality import get_modality
from event import Event

class Text():
    def __init__(self, id=None, name=None):
        self.id = None
        self.name = name
        self.relations_union_count = 0
        self.relations_intersection_count = 0
        self.annotator = []
        self.relations_union = []
        self.relations_intersection = []
        self.events_union = []

    def set_annotator(self, annotator):
        self.annotator.append(annotator)

    """Since different annotators annotate different events we might
    be interested in the union of all events for a textfile"""
    def compute_union_events(self):
        del self.events_union[:]

        all_in_one = []
        for ann in self.annotator:
            all_in_one = all_in_one + ann.events

        # x if the word contained in x is not already in our list of words so far
        self.events_union = [x for i, x in enumerate(all_in_one) if x.content not in [y.content for y in all_in_one[:i]]]

    """Since different annotators annotate different relations we might
    want to know which relations all annotators for a textfile have in common (intersection)"""
    def compute_intersection_relations(self):
        del self.relations_intersection[:]
        self.relations_intersection_count = 0

        relations = []
        relations_tmp = []

        for rel in self.annotator[0].relations:
            relations_tmp.append(rel)

        for ann in self.annotator[1:]:
            # Add rel to list if we have rel already in relations_tmp[]
            for rel in ann.relations:
                if rel.identifier in [x.identifier for x in relations_tmp]:
                    relations.append(rel)

            del relations_tmp[:]
            relations_tmp = deepcopy(relations)

        self.relations_intersection = relations
        self.relations_intersection_count = len(self.relations_intersection)

    """Union over all relations annotated in a certain textfile"""
    def compute_union_relations(self):
        del self.relations_union[:]
        self.relations_union= 0

        # Put all relations from all annotators in one list
        relations = []
        for ann in self.annotator:
            for rel in ann.relations:
                relations.append({rel.identifier : rel})

        # Go through all relations and add a relation to a list if
        # the identifier of the relation is not already in the list
        union = []
        for r in relations:
            if r.keys()[0] not in [x.keys()[0] for x in union]:
                union.append(r)

        self.relations_union = [x.values()[0] for x in union]
        self.relations_union_count = len(self.relations_union)

class Relation():
    def __init__(self, parent=None, source=None, target=None, time_type=None):
        self.parent = parent
        self.source = source
        self.target = target
        self.identifier = None

        if time_type in ["same_as", "overlap", "after", "is_contained_in", "before", "contains", "includes", "is_included", "no relations"]:
            self.time_type = time_type
        else:
            self.time_type = None

    def set_time_type(self, time_type):
        if time_type in ["same_as", "overlap", "after", "is_contained_in", "before", "contains", "includes", "is_included", "no relations"]:
            self.time_type = time_type
        else:
            self.time_type = None

    def set_source(self, source):
        self.source = source

    def set_target(self, target):
        self.target = target

    def set_identifier(self):
        self.identifier = str(self.source.begin)+str(self.source.end)+str(self.target.begin)+str(self.target.end)


class Annotator():
    def __init__(self, id=None, xml_id=None):
        self.parent = None
        self.events = []
        self.relations = []
        self.id = id
        self.xml_id = xml_id


class Holder():
    textfiles = []


# filename of xml File and dirname to the directory where the corresponding texts are
def parseXML(filename, dirname):
    tree = etree.parse(filename)
    root = tree.getroot()

    data = Holder()

    for i, txt in enumerate(root.iterdescendants("file")):
        # Create Text object
        text = Text(i, txt.get("name"))

        for j, ann in enumerate(txt.iterdescendants("annotator")):
            # Create an Annotator object
            annotator = Annotator(j, ann.get("id"))
            annotator.parent = text

            # Create link from Text object
            text.set_annotator(annotator)

            for k, ev in enumerate(ann.iterdescendants("event")):
                event_text = ev.get("text")

                # Get the surrounding text and sentence for this event
                sentence = get_sentence(event_text, text.name, dirname, int(ev.get("begin")))[0]
                surrounding = get_surrounding(event_text, text.name, dirname, int(ev.get("begin")), Event.surrounding_words_left, Event.surrounding_words_right)

                pos_surrounding = get_surrounding(event_text, text.name, dirname, int(ev.get("begin")), Event.pos_surrounding_words_left, Event.pos_surrounding_words_right)
                # Get the polarity of the event
                polarity = get_polarity(surrounding)

                # Get the modality of the event
                modality = get_modality(surrounding)

                # Create an Event object
                event = Event(annotator, k, event_text, sentence, surrounding, pos_surrounding, polarity, modality, ev.get("begin"), ev.get("end"))
                # Create link from Annotator object
                annotator.events.append(event)

            for k, tlink in enumerate(ann.iterdescendants("tlink")):
                # Create a Relation object
                relation = Relation()
                relation.parent = annotator
                relation.id = k
                relation.set_time_type(tlink[0].get("type"))

                # Create link from Annotator object
                annotator.relations.append(relation)

                # Connect corresponding event objects to this relation object
                # Doing this by going through all possible events
                source = tlink[1]
                begin = source.get("begin")
                end = source.get("end")

                # Search through the events of this annotator
                for event in annotator.events:
                    if event.begin == int(begin) and event.end == int(end):
                        relation.set_source(event)
                        break

                target = tlink[2]
                begin = target.get("begin")
                end = target.get("end")

                for event in annotator.events:
                    if event.begin == int(begin) and event.end == int(end):
                        relation.set_target(event)
                        break

                # Identifier, so we can identify two relations which are the same
                relation.set_identifier()

        # Include text to data structure
        data.textfiles.append(text)

    return data
