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
