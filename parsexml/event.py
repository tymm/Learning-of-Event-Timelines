class Event():

    """Instances of this class are used to describe an event from fables-100-temporal-dependency.xml.

    Class variables:
        surrounding_words_right (int): Determines how many words to the right of the event will be included in the surrounding instance variable.
        surrounding_words_left (int): Same as above but to the left of the event.
        pos_surrounding_words_(left|right) (int): Same as above for the POS surrounding area.

    """

    surrounding_words_left = 3
    surrounding_words_right = 2
    pos_surrounding_words_left = 1
    pos_surrounding_words_right = 1

    def __init__(self, parent=None, id_=None, content=None, sentence=None, num_words_as_event_before_event=None, surrounding=None, pos_surrounding=None, polarity=None, modality=None, begin=None, end=None):
        """Constructor of the Event class

        Args:
            parent (Annotator): Reference to the Annotator object which describes the parent node of the event.
            id_ (int): Unique id (not needed so far).
            content (str): The events text.
            sentence (str): Text of the sentence the event is in.
            num_words_as_event_before_event (int): Number of words before the event which are the same as the event. Needed to identify the exact position of an event in a sentence.
            surrounding (str): The text of the surrounding area of the event (including the event).
            pos_surrounding (list): POS tags of surrounding text (including the event).
            polarity (bool): Grammatical polarity. Describes if the area set by the surrounding argument is affirmative or negative.
            modality (bool): Grammatical modality. Describes the presence of auxiliaries.
            begin (int): Position in the corresponding text where the event begins.
            end (int): Position in the corresponding text where the event ends.

        """
        self.parent = parent
        self.id_ = id_
        self.content = content
        self.sentence = sentence
        self.num_words_as_event_before_event = num_words_as_event_before_event
        self.surrounding = surrounding
        self.pos_surrounding = pos_surrounding
        self.polarity = polarity
        self.modality = modality
        self.begin = int(begin)
        self.end = int(end)
