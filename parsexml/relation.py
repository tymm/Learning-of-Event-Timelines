from temporalrelation import TemporalRelation

class Relation():

    """Instances of this class are used to describe temporal relations between events in the fables referenced to by fables-100-temporal-dependency.xml"""

    def __init__(self, parent=None, source=None, target=None, temporal_rel=None):
        """Constructor of the Relation class

        Args:
            parent (Annotator): Reference to the Annotator object above the relation in the xml hierarchy.
            source (Event): Reference to the source Event object corresponding to the relation.
            target (Event): Same as above for the target event.
            temporal_rel (TemporalRelation): Describes the temporal relation for a relation.

        Attributes:
            identifier (str): Unique identification for a relation. Needed for identification of two relations which are the same.

        """
        self.parent = parent
        self.source = source
        self.target = target
        self.identifier = None

        self.determine_temporal_rel(temporal_rel)

    def set_temporal_rel(self, temporal_rel):
        self.determine_temporal_rel(temporal_rel)

    def determine_temporal_rel(self, temporal_rel):
        if temporal_rel in ["same_as", "overlap", "is_contained_in", "contains", "no relations"]:
            self.temporal_rel = TemporalRelation.NONE
        elif temporal_rel == "before":
            self.temporal_rel = TemporalRelation.BEFORE
        elif temporal_rel == "after":
            self.temporal_rel = TemporalRelation.BEFORE
            tmp = self.source
            self.source = self.target
            self.target = tmp
        elif temporal_rel == "includes":
            self.temporal_rel = TemporalRelation.INCLUDES
        elif temporal_rel == "is_included":
            self.temporal_rel = TemporalRelation.IS_INCLUDED
        else:
            self.temporal_rel = None

    def set_source(self, source):
        self.source = source

    def set_target(self, target):
        self.target = target

    def set_identifier(self):
        self.identifier = str(self.source.begin)+str(self.source.end)+str(self.target.begin)+str(self.target.end)
