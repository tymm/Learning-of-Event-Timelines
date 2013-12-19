from lxml import etree

class Text():
    def __init__(self, id=None, name=None):
        self.id = None
        self.name = name
        self.relations_union_count = 0
        self.relations_intersection_count = 0
        self.annotator = []
        self.relations_union = []
        self.relations_intersection = []

    def set_annotator(self, annotator):
        self.annotator.append(annotator)

class Event():
    def __init__(self, parent=None, id=None, content=None, begin=None, end=None):
        self.parent = parent
        self.id = id
        self.content = content
        self.begin = begin
        self.end = end

class Relation():
    def __init__(self, parent=None, source=None, target=None, time_type=None):
        self.parent = parent
        self.source = source
        self.target = target
        self.identifier = None

        if time_type in ["same_as", "overlap", "after", "is_contained_in", "before", "contains"]:
            self.time_type = time_type
        else:
            self.time_type = None

    def set_time_type(self, time_type):
        if time_type in ["same_as", "overlap", "after", "is_contained_in", "before", "contains"]:
            self.time_type = time_type
        else:
            self.time_type = None

    def set_identifier(self, source_begin, source_end, target_begin, target_end):
        self.identifier = source_begin+source_end+target_begin+target_end

class Annotator():
    def __init__(self, id=None, xml_id=None):
        self.parent = None
        self.events = []
        self.relation = []
        self.id = id
        self.xml_id = xml_id


class Holder():
    textfiles = []


def parseXML(filename):
    tree = etree.parse(filename)
    root = tree.getroot()

    data = Holder()

    for i, txt in enumerate(root.iterdescendants("file")):
        # Create Text object
        text = Text(i, txt.get("name"))

        for j, ann in enumerate(txt.iterdescendants("annotator")):
            # Create an Annotator object
            annotator = Annotator(j, ann.get("id"))

            # Create link from Text object
            text.set_annotator(annotator)

            for k, ev in enumerate(ann.iterdescendants("event")):
                # Create an Event object
                event = Event(annotator, k, ev.get("text"), ev.get("begin"), ev.get("end"))
                # Create link from Annotator object
                annotator.events.append(event)

            for k, tlink in enumerate(ann.iterdescendants("tlink")):
                # Create a Relation object
                relation = Relation()
                relation.parent = annotator
                relation.id = k
                relation.set_time_type(tlink[0].get("type"))

                # Create link from Annotator object
                annotator.relation.append(relation)

                # Lets figure out which events we have
                source = tlink[1]
                begin = source.get("begin")
                end = source.get("end")

                # Search through the events of this annotator
                for event in annotator.events:
                    if event.begin == begin and event.end == end:
                        relation.source = event
                        break

                target = tlink[2]
                begin = target.get("begin")
                end = target.get("end")

                for event in annotator.events:
                    if event.begin == begin and event.end == end:
                        relation.target = event
                        break

                # Identifier, so we can identify two relations which are the same
                relation.set_identifier(relation.source.begin, relation.source.end, relation.target.begin, relation.target.end)

        # Include text to data structure
        data.textfiles.append(text)

    return data

a = parseXML("fables-100-temporal-dependency.xml")
print a.textfiles[1].name
print a.textfiles[1].annotator[0].events
print a.textfiles[1].annotator[1].events
