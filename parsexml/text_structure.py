import nltk.data
from parsexml.sentence import Sentence
from collections import OrderedDict

class Text_structure:
    TEXTDIR = "McIntyreLapata09Resources/fables/"

    def __init__(self, annotator_obj):
        self.annotator_obj = annotator_obj
        self.filename = self.annotator_obj.parent.name

        # {Sentence: [Event, Event, ...], Sentence: [...], ...}
        self.structure = OrderedDict()

        self.sentences = self._get_sentence_objs()
        self._build_structure()

    def _get_sentence_objs(self):
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

        text = self._get_text()
        sentences_text = sent_detector.tokenize(text)

        # Get start and beginning for every sentence
        sentences = map(self._create_sentence_obj, sentences_text)

        return sentences

    def _create_sentence_obj(self, text):
        #text = text.replace("\r\n", "")
        return Sentence(text, self.filename)

    def _get_text(self):
        with open(Text_structure.TEXTDIR + self.filename, "r") as f:
            text = f.read()

        return text

    def _build_structure(self):
        for sentence in self.sentences:
            # Add sentence to structure if necessary
            if sentence not in self.structure:
                self.structure.update({sentence: []})

            for event in self.annotator_obj.events:
                if event.begin >= sentence.begin and event.end <= sentence.end:
                    # Append event to sentence in structure
                    self.structure[sentence].append(event)
