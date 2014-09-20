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
        self.temporal_rel = self.determine_temporal_rel(temporal_rel)

    def determine_temporal_rel(self, temporal_rel):
        if temporal_rel == "none":
            return TemporalRelation.NONE
        elif temporal_rel == "before":
            return TemporalRelation.BEFORE
        # "after" is just a reversed "before" relation
        elif temporal_rel == "after":
            tmp = self.source
            self.source = self.target
            self.target = tmp
            return TemporalRelation.BEFORE
        elif temporal_rel == "includes":
            return TemporalRelation.INCLUDES
        elif temporal_rel == "is_included":
            return TemporalRelation.IS_INCLUDED
        else:
            return None

    def set_source(self, source):
        self.source = source

    def set_target(self, target):
        self.target = target

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(self.parent.parent.name+str(self.source.begin)+str(self.source.end)+str(self.target.begin)+str(self.target.end)+str(self.temporal_rel))
