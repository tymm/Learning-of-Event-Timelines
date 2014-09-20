class Sentence:
    TEXTDIR = "McIntyreLapata09Resources/fables/"

    def __init__(self, text, filename):
        self.text = text
        self.filename = filename
        self.begin = self._get_beginning()
        self.end = self._get_ending()

    def __eq__(self, other):
        return self.text == other.text

    def __hash__(self):
        return hash(self.text)

    def _get_beginning(self):
        with open(Sentence.TEXTDIR + self.filename, "r") as f:
            text = f.read()
            #text = text.replace("\r\n", "")

            beginning = text.find(self.text)

            if beginning == -1:
                raise CouldNotFindBeginningOfSentence(self.text, self.filename)
            else:
                return beginning

    def _get_ending(self):
        return self.begin + len(self.text)

class CouldNotFindBeginningOfSentence(Exception):
    def __init__(self, text, filename):
        self.text = text
        self.filename = filename

    def __str__(self):
        return repr("Could not find the beginning position of \"" + self.text + "\" in file: "+ self.filename +".")
