class Text():

    """Instances of this class are used to describe the fables referenced to by fables-100-temporal-dependency.xml"""

    def __init__(self, id_=None, name=None):
        """Constructor of the Text class

        Args:
            id_ (int): Unique id (not needed so far).
            name (str): Name of the text file the fable is in

        Attributes:
            relations_union_count (int): Count of the union of all relations of events in a text
            relations_intersection_count (int): Same as above for intersections
            annotator (list): Will contain all Annotator objects corresponding to a Text Object
            relations_union (list): Will contain all Relation objects (unions) corresponding to a Text Object
            relations_intersection (list): Same as above for intersections
            events_union (list): Will contain all Event Objects corresponding to a Text Object

        """
        self.id_ = None
        self.name = name
        self.relations_union_count = 0
        self.relations_intersection_count = 0
        self.annotator = []
        self.relations_union = []
        self.relations_intersection = []
        self.events_union = []

    def append_annotator(self, annotator):
        """Appends an Annotator object to the list of Annotator objects."""
        self.annotator.append(annotator)

    def compute_union_events(self):
        """Gets all union events and appends the Event objects to the list of union Event objects.

        This could be interesting because different annotators often annotate different events for the same text.
        """
        del self.events_union[:]

        all_in_one = []
        for ann in self.annotator:
            all_in_one = all_in_one + ann.events

        # x if the word contained in x is not already in our list of words so far
        self.events_union = [x for i, x in enumerate(all_in_one) if x.content not in [y.content for y in all_in_one[:i]]]

    def compute_intersection_relations(self):
        """Gets all intersecting relations and appends the Relation objects to the list of intersecting Relation objects.

        This could be interesting because different annotators often annotate different relations for the same text.
        """
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

    def compute_union_relations(self):
        """Gets all union relations and appends the Relation objects to the list of union Relation objects.

        This could be interesting because different annotators often annotate different relations for the same text.
        """
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
