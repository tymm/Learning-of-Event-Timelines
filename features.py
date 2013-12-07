from lxml import etree

class Text():
    id = None
    name = None
    annotator = []

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

class Event():
    parent = None
    id = None
    content = None
    begin = None
    end = None

    def __init__(self, parent=None, id=None, content=None, begin=None, end=None):
        self.parent = parent
        self.id = id
        self.content = content
        self.begin = begin
        self.end = end

class Relation():
    parent = None
    source = None
    target = None
    time_type = None

    def __init__(self, parent=None, source=None, target=None, time_type=None):
        self.parent = parent
        self.source = source
        self.target = target

        if time_type in ["is_contained_in", "before", "contains"]:
            self.time_type = time_type
        else:
            self.time_type = None

    def set_time_type(self, time_type):
        if time_type in ["is_contained_in", "before", "contains"]:
            self.time_type = time_type
        else:
            self.time_type = None

class Annotator():
    parent = None
    id = None
    xml_id = None
    event = []
    relation = []

    def __init__(self, parent=None, id=None, xml_id=None):
        self.parent = parent
        self.id = id
        self.xml_id = xml_id


class Holder():
    text = []


tree = etree.parse("fables-100-temporal-dependency.xml")
root = tree.getroot()

data = Holder()

for i, txt in enumerate(root.iterdescendants("file")):
    # Create Text object
    text = Text(i, txt.get("name"))
    # Include text to data structure
    data.text.append(text)

    for j, ann in enumerate(txt.iterdescendants("annotator")):
        # Create an Annotator object
        annotator = Annotator(text, j, ann.get("id"))
        # Create link from Text object
        text.annotator.append(annotator)

        for k, ev in enumerate(ann.iterdescendants("event")):
            # Create an Event object
            event = Event(annotator, k, ev.get("text"), ev.get("begin"), ev.get("end"))
            # Create link from Annotator object
            annotator.event.append(event)

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
            for event in annotator.event:
                if event.begin == begin and event.end == end:
                    relation.source = event
                    break

            target = tlink[2]
            begin = target.get("begin")
            end = target.get("end")

            for event in annotator.event:
                if event.begin == begin and event.end == end:
                    relation.target = event
                    break


print data.text
