import unittest
from cStringIO import StringIO
from helper import get_surrounding, preprocess_sentence
from polarity import get_polarity
from modality import get_modality
from tense import get_tense
from aspect import get_aspect

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

class PolarityGuessing(unittest.TestCase):
    def test_Dont(self):
        text = "They don't like it at all"
        self.assertEqual(get_polarity(text), 1)

    def test_Dont_2(self):
        text = "They dont like it at all"
        self.assertEqual(get_polarity(text), 1)

    def test_DoNot(self):
        text = "They do not like it at all"
        self.assertEqual(get_polarity(text), 1)

    def test_Not(self):
        text = "I have not gone"
        self.assertEqual(get_polarity(text), 1)

    def test_Not_2(self):
        text = "He does not go"
        self.assertEqual(get_polarity(text), 1)

    def test_Affirmative(self):
        text = "They like it very much"
        self.assertEqual(get_polarity(text), 0)

    def test_Affirmative_2(self):
        text = "I see him"
        self.assertEqual(get_polarity(text), 0)

class ModalityGuessing(unittest.TestCase):
    def test_Would(self):
        text = "were true, one would have seen it on CNN."
        self.assertEqual(get_modality(text), 1)

    def test_NoModal(self):
        text = "I like it a lot"
        self.assertEqual(get_modality(text), 0)

class TenseGuessing(unittest.TestCase):
    def test_SimplePresent(self):
        text = "I work long hours in front of the computer every day"
        self.assertEqual(get_tense(text), 0)

    def test_SimplePresent_2(self):
        text = "He doesn't work at night usually"
        self.assertEqual(get_tense(text), 0)

    def test_SimplePresent_3(self):
        text = "He never goes home to his family"
        self.assertEqual(get_tense(text), 0)

    def test_PresentProgressive(self):
        text = "I'm working at the moment"
        self.assertEqual(get_tense(text), 1)

    def test_PresentProgressive_2(self):
        text = "He isn't working now at all"
        self.assertEqual(get_tense(text), 1)

    def test_PresentProgressive_3(self):
        text = "I'm not going"
        self.assertEqual(get_tense(text), 1)

    def test_SimplePast(self):
        text = "He went to America in 1990"
        self.assertEqual(get_tense(text), 2)

    def test_SimplePast_2(self):
        text = "He didn't work yesterday"
        self.assertEqual(get_tense(text), 2)

    def test_SimplePast_3(self):
        text = "Last wednesday I didn't work at the cinema"
        self.assertEqual(get_tense(text), 2)

    def test_PastProgressive(self):
        text = "While I was doing my homework"
        self.assertEqual(get_tense(text), 3)

    def test_PastProgressive_2(self):
        text = "He wasn't working"
        self.assertEqual(get_tense(text), 3)

    def test_PastProgressive_3(self):
        text = "He wasn't going"
        self.assertEqual(get_tense(text), 3)

    def test_SimplePresentPerfect(self):
        text = "I have gone already"
        self.assertEqual(get_tense(text), 4)

    def test_SimplePresentPerfect_2(self):
        text = "He hasn't gone so far"
        self.assertEqual(get_tense(text), 4)

    def test_SimplePresentPerfect_3(self):
        text = "I haven't worked ever"
        self.assertEqual(get_tense(text), 4)

    def test_SimplePresentPerfect_4(self):
        text = "I haven't seen him for a while now"
        self.assertEqual(get_tense(text), 4)

    def test_PresentPerfectProgressive(self):
        text = "I have been working all day"
        self.assertEqual(get_tense(text), 5)

    def test_PresentPerfectProgressive_2(self):
        text = "Since when has he been going?"
        self.assertEqual(get_tense(text), 5)

    def test_PresentPerfectProgressive_3(self):
        text = "I haven't been working for a long time"
        self.assertEqual(get_tense(text), 5)

    def test_PresentPerfectProgressive_4(self):
        text = "He has been working since yesterday"
        self.assertEqual(get_tense(text), 5)

    def test_PresentPerfectProgressive_5(self):
        text = "Has he been going?"
        self.assertEqual(get_tense(text), 5)

    def test_PresentPerfectProgressive_6(self):
        text = "Have I been going?"
        self.assertEqual(get_tense(text), 5)

    def test_SimplePastPerfect(self):
        text = "She never had gone there"
        self.assertEqual(get_tense(text), 6)

    def test_SimplePastPerfect_2(self):
        text = "I hadn't worked already"
        self.assertEqual(get_tense(text), 6)

    def test_SimplePastPerfect_3(self):
        text = "He just had gone"
        self.assertEqual(get_tense(text), 6)

    def test_SimplePastPerfect_4(self):
        text = "Had he gone already?"
        self.assertEqual(get_tense(text), 6)

    def test_PastPerfectProgressive(self):
        text = "I had been working"
        self.assertEqual(get_tense(text), 7)

    def test_PastPerfectProgressive_2(self):
        text = "Had I been going?"
        self.assertEqual(get_tense(text), 7)

    def test_PastPerfectProgressive_3(self):
        text = "He had been going for 2 hours"
        self.assertEqual(get_tense(text), 7)

    def test_WillFuture(self):
        text = "He won't work"
        self.assertEqual(get_tense(text), 8)

    def test_WillFuture_2(self):
        text = "He'll go"
        self.assertEqual(get_tense(text), 8)

    def test_WillFuture_3(self):
        text = "Will he go?"
        self.assertEqual(get_tense(text), 8)

class AspectGuessing(unittest.TestCase):
    def test_SimpleAspect(self):
        text = "I went"
        self.assertEqual(get_aspect(text), "simple")

    def test_SimpleAspect_2(self):
        text = "I will go"
        self.assertEqual(get_aspect(text), "simple")

    def test_SimpleAspect_3(self):
        text = "They clean the window"
        self.assertEqual(get_aspect(text), "simple")

    def test_SimpleAspect_4(self):
        text = "Shall we go?"
        self.assertEqual(get_aspect(text), "simple")

    def test_SimpleAspect_5(self):
        text = "Will we go there?"
        self.assertEqual(get_aspect(text), "simple")

    def test_PerfectAspect(self):
        text = "I had cleaned the whole kitchen"
        self.assertEqual(get_aspect(text), "perfect")

    def test_PerfectAspect_2(self):
        text = "They will have eaten"
        self.assertEqual(get_aspect(text), "perfect")

    def test_PerfectAspect_3(self):
        text = "Yesterday it has found"
        self.assertEqual(get_aspect(text), "perfect")

    def test_PerfectAspect_4(self):
        text = "She has taken all her belongings"
        self.assertEqual(get_aspect(text), "perfect")

    def test_PerfectAspect_5(self):
        text = "Will they have eaten?"
        self.assertEqual(get_aspect(text), "perfect")

    def test_ProgressiveAspect(self):
        text = "She will have been singing"
        self.assertEqual(get_aspect(text), "progressive")

    def test_ProgressiveAspect_2(self):
        text = "They have been fighting for the whole day."
        self.assertEqual(get_aspect(text), "progressive")

    def test_ProgressiveAspect_3(self):
        text = "She had been flying to Vancouver"
        self.assertEqual(get_aspect(text), "progressive")

    def test_ProgressiveAspect_4(self):
        text = "Will she have been singing?"
        self.assertEqual(get_aspect(text), "progressive")


if __name__ == '__main__':
    unittest.main()
