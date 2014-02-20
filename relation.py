class Relation():

    """Instances of this class are used to describe temporal relations between events in the fables referenced to by fables-100-temporal-dependency.xml"""

    def __init__(self, parent=None, source=None, target=None, time_type=None):
        """Constructor of the Relation class

        Args:
            parent (Annotator): Reference to the Annotator object above the relation in the xml hierarchy.
            source (Event): Reference to the source Event object corresponding to the relation.
            target (Event): Same as above for the target event.
            time_type (str): Describes the type of time relation for a relation.

        Attributes:
            identifier (str): Unique identification for a relation. Needed for identification of two relations which are the same.

        """
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
