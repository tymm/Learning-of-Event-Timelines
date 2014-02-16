import unittest
from cStringIO import StringIO
from helper import get_surrounding, preprocess_sentence 

class TextProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result_text = "finger and thumb he said or rather shouted so"

    def test_EasySentence(self):
        r = get_surrounding("said", "EasySentence.txt", "test", 43, 4, 4)
        self.assertEqual(r, self.result_text)

    def test_EventAtBeginning(self):
        r = get_surrounding("Holding", "EasySentence.txt", "test", 0, 4, 4)
        self.assertEqual(r, "Holding it between his finger")

    def test_EventAtEnd(self):
        r = get_surrounding("so", "EasySentence.txt", "test", 66, 4, 4)
        self.assertEqual(r, "said or rather shouted so")

    def test_CommaSentence(self):
        r = get_surrounding("said", "CommaSentence.txt", "test", 44, 4, 4)
        self.assertEqual(r, self.result_text)

    def test_HyphenSentence(self):
        r = get_surrounding("said", "HyphenSentence.txt", "test", 43, 4, 4)
        self.assertEqual(r, self.result_text)

    def test_ComplicatedSentence(self):
        r = get_surrounding("said", "ComplicatedSentence.txt", "test", 44, 4, 4)
        self.assertEqual(r, self.result_text)

    def test_SemicolonSentence(self):
        r = get_surrounding("try", "SemicolonSentence.txt", "test", 31, 4, 4)
        self.assertEqual(r, "Wind had the first try and gathering up all")

    def test_ApostropheInTheBeginning(self):
        r = get_surrounding("came", "ApostropheBeginningSentence.txt", "test", 32, 4, 4)
        self.assertEqual(r, "sure enough in he came and made a great")

    def test_ConnectedWordsSentence(self):
        r = get_surrounding("to-do", "ConnectedWordsSentence.txt", "test", 55, 4, 4)
        self.assertEqual(r, "and made a great to-do about the way the")

    def test_LegitimateUseOfApostrophe(self):
        r = get_surrounding("don't", "LegitimateUseOfApostrophe.txt", "test", 5, 4, 4)
        self.assertEqual(r, "They don't want to be there")

class FileProcessing(unittest.TestCase):
    def test_UnwantedCharacterStripping(self):
        text = """Holding it between his finger and thumb, he said--or rather shouted, so angry was he--"Who
are you, pray, you wretched little
creature, that you make so free with , my person?"""

        new_text = preprocess_sentence(text)
        self.assertEqual(new_text, 'Holding it between his finger and thumb he said or rather shouted so angry was he Who are you pray you wretched little creature that you make so free with my person')

if __name__ == '__main__':
    unittest.main()
