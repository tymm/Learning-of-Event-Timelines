import unittest
from cStringIO import StringIO
from feature.preprocessing.text import get_surrounding, preprocess_sentence
from feature.preprocessing.polarity import get_polarity
from feature.preprocessing.modality import get_modality
from feature.preprocessing.tense import get_tense, Tenses
from feature.preprocessing.aspect import get_aspect, Aspects
from feature.preprocessing.text import preprocess_sentence
from parsexml.text_structure import Text_structure
from parser import parse_XML

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

    """
    def test_LegitimateUseOfApostrophe(self):
        r = get_surrounding("don't", "LegitimateUseOfApostrophe.txt", "test", 5, 4, 4)
        self.assertEqual(r, "They do not want to be there")
        """

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
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "work", 0), Tenses.present)

    def test_SimplePresent_2(self):
        text = "He doesn't work at night usually"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "work", 0), Tenses.present)

    def test_SimplePresent_3(self):
        text = "He never goes home to his family"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "goes", 0), Tenses.present)

    def test_SimplePresent_4(self):
        text = "to come and settle in the"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "settle", 0), Tenses.present)

    # Tagger does tag consulting as NN
    #def test_SimplePresent_5(self):
        #text = "eyes and after consulting a Doctor"
        #self.assertEqual(get_tense(text, "consulting", 0), Tenses.present)

    def test_SimplePresent_6(self):
        text = "catching sight of some"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "catching", 0), Tenses.present)

    def test_SimplePresent_8(self):
        text = "the Sun each claiming that he"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "claiming", 0), Tenses.present)

    def test_SimplePresent_9(self):
        text = "a neighbouring pool intending to drown"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "intending", 0), Tenses.present)

    def test_PresentProgressive(self):
        text = "I'm working at the moment"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "working", 0), Tenses.present)

    def test_PresentProgressive_2(self):
        text = "He isn't working now at all"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "working", 0), Tenses.present)

    def test_PresentProgressive_3(self):
        text = "I'm not going"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "going", 0), Tenses.present)

    def test_Present(self):
        text = "Coming and standing under the"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "coming", 0), Tenses.present)

    def test_Present_2(self):
        text = "Observing it to"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "observing", 0), Tenses.present)

    def test_Present_2(self):
        text = "among some Reeds growing by the"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "growing", 0), Tenses.present)

    def test_SimplePast(self):
        text = "He went to America in 1990"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "went", 0), Tenses.past)

    def test_SimplePast_2(self):
        text = "He didn't work yesterday"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "work", 0), Tenses.past)

    def test_SimplePast_3(self):
        text = "Last wednesday I didn't work at the cinema"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "work", 0), Tenses.past)

    # Tagger doesn't know "heard"
    #def test_SimplePast_4(self):
        #text = "A cat heard of this"
        #self.assertEqual(get_tense(text, "heard", 0), Tenses.past)

    # Tagger doesn't know "met" in that context
    #def test_SimplePast_5(self):
        #text = "all the Mice met together in"
        #self.assertEqual(get_tense(text, "met", 0), Tenses.past)

    # Tagger tags "stole" the wrong way
    #def test_SimplePast_6(self):
        #text = "but who daily stole a portion"
        #self.assertEqual(get_tense(text, "stole", 0), Tenses.past)

    def test_PastProgressive(self):
        text = "While I was doing my homework"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "doing", 0), Tenses.past)

    def test_PastProgressive_2(self):
        text = "He wasn't working"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "working", 0), Tenses.past)

    def test_PastProgressive_3(self):
        text = "He wasn't going"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "going", 0), Tenses.past)

    def test_SimplePresentPerfect(self):
        text = "I have gone already"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "gone", 0), Tenses.present)

    def test_SimplePresentPerfect_2(self):
        text = "He hasn't gone so far"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "gone", 0), Tenses.present)

    def test_SimplePresentPerfect_3(self):
        text = "I haven't worked ever"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "worked", 0), Tenses.present)

    def test_SimplePresentPerfect_4(self):
        text = "I haven't seen him for a while now"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "seen", 0), Tenses.present)

    def test_PresentPerfectProgressive(self):
        text = "I have been working all day"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "working", 0), Tenses.present)

    def test_PresentPerfectProgressive_2(self):
        text = "Since when has he been going?"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "going", 0), Tenses.present)

    def test_PresentPerfectProgressive_3(self):
        text = "I haven't been working for a long time"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "working", 0), Tenses.present)

    def test_PresentPerfectProgressive_4(self):
        text = "He has been working since yesterday"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "working", 0), Tenses.present)

    def test_PresentPerfectProgressive_5(self):
        text = "Has he been going?"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "going", 0), Tenses.present)

    def test_PresentPerfectProgressive_6(self):
        text = "Have I been going?"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "going", 0), Tenses.present)

    def test_SimplePastPerfect(self):
        text = "She never had gone there"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "gone", 0), Tenses.past)

    def test_SimplePastPerfect_2(self):
        text = "I hadn't worked already"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "worked", 0), Tenses.past)

    def test_SimplePastPerfect_3(self):
        text = "He just had gone"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "gone", 0), Tenses.past)

    def test_SimplePastPerfect_4(self):
        text = "Had he gone already?"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "gone", 0), Tenses.past)

    def test_PastPerfectProgressive(self):
        text = "I had been working"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "working", 0), Tenses.past)

    def test_PastPerfectProgressive_2(self):
        text = "Had I been going?"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "going", 0), Tenses.past)

    def test_PastPerfectProgressive_3(self):
        text = "He had been going for 2 hours"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "going", 0), Tenses.past)

    def test_WillFuture(self):
        text = "He won't work"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "work", 0), Tenses.future)

    def test_WillFuture_2(self):
        text = "He'll go"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "go", 0), Tenses.future)

    def test_WillFuture_3(self):
        text = "Will he go?"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "go", 0), Tenses.future)

    def test_Future(self):
        text = "He is going to visit"
        text = preprocess_sentence(text)
        self.assertEqual(get_tense(text, "visit", 0), Tenses.future)

class AspectGuessing(unittest.TestCase):
    def test_PerfectAspect(self):
        text = "I had cleaned the whole kitchen"
        self.assertEqual(get_aspect(text), Aspects.perfect)

    def test_PerfectAspect_2(self):
        text = "They will have eaten"
        self.assertEqual(get_aspect(text), Aspects.perfect)

    def test_PerfectAspect_3(self):
        text = "Yesterday it has found"
        self.assertEqual(get_aspect(text), Aspects.perfect)

    def test_PerfectAspect_4(self):
        text = "She has taken all her belongings"
        self.assertEqual(get_aspect(text), Aspects.perfect)

    def test_PerfectAspect_5(self):
        text = "Will they have eaten?"
        self.assertEqual(get_aspect(text), Aspects.perfect)

    def test_Perfect_ProgressiveAspect(self):
        text = "She will have been singing"
        self.assertEqual(get_aspect(text), Aspects.perfect_progressive)

    def test_Perfect_ProgressiveAspect_2(self):
        text = "They have been fighting for the whole day."
        self.assertEqual(get_aspect(text), Aspects.perfect_progressive)

    def test_Perfect_ProgressiveAspect_3(self):
        text = "She had been flying to Vancouver"
        self.assertEqual(get_aspect(text), Aspects.perfect_progressive)

    def test_Perfect_ProgressiveAspect_4(self):
        text = "Will she have been singing?"
        self.assertEqual(get_aspect(text), Aspects.perfect_progressive)

    def test_ProgressiveAspect(self):
        text = "I am eating so much everyday!"
        self.assertEqual(get_aspect(text), Aspects.progressive)

    def test_ProgressiveAspect_2(self):
        text = "I was eating so much everyday!"
        self.assertEqual(get_aspect(text), Aspects.progressive)

    def test_ProgressiveAspect_3(self):
        text = "I will be eating so much everyday!"
        self.assertEqual(get_aspect(text), Aspects.progressive)

    def test_ProgressiveAspect_3(self):
        text = "I would be eating so much everyday!"
        self.assertEqual(get_aspect(text), Aspects.progressive)

class TextStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load data
        data = parse_XML("fables-100-temporal-dependency.xml", Text_structure.TEXTDIR)

        # Find 1.txt
        text_obj = None
        for text in data.textfiles:
            if text.name == "1.txt":
                text_obj = text
                break

        # Find 7.txt
        text_obj_two = None
        for text in data.textfiles:
            if text.name == "7.txt":
                text_obj_two = text
                break

        # Find 3.txt
        text_obj_three = None
        for text in data.textfiles:
            if text.name == "3.txt":
                text_obj_three = text
                break

        cls.structure = text_obj.annotator[0].text_structure.structure
        cls.sentences = [s for s in cls.structure]
        cls.events = text_obj.annotator[0].events

        cls.structure_two = text_obj_two.annotator[0].text_structure.structure
        cls.sentences_two = [s for s in cls.structure_two]
        cls.events_two = text_obj_two.annotator[0].events

        cls.structure_three = text_obj_three.annotator[0].text_structure.structure
        cls.sentences_three = [s for s in cls.structure_three]
        cls.events_three = text_obj_three.annotator[0].events

    def test_IsOrderOfSentenceRight(self):
        self.assertEqual(self.sentences[0].text, "A hungry Fox saw some fine bunches of Grapes hanging from a vine that \r\nwas trained along a high trellis, and did his best to reach them by \r\njumping as high as he could into the air.")
        self.assertEqual(self.sentences[1].text, "But it was all in vain, for \r\nthey were just out of reach: so he gave up trying, and walked away \r\nwith an air of dignity and unconcern, remarking, \"I thought those \r\nGrapes were ripe, but I see now they are quite sour.\"")

        self.assertEqual(self.sentences_two[0].text, "A Bat fell to the ground and was caught by a Weasel, and was just \r\ngoing to be killed and eaten when it begged to be let go.")
        self.assertEqual(self.sentences_two[1].text, "The Weasel \r\nsaid he couldn't do that because he was an enemy of all birds on \r\nprinciple.")
        self.assertEqual(self.sentences_two[2].text, "\"Oh, but,\" said the Bat, \"I'm not a bird at all: I'm a \r\nmouse.\"")
        self.assertEqual(self.sentences_two[3].text, "\"So you are,\" said the Weasel, \"now I come to look at you\"; \r\nand he let it go.")
        self.assertEqual(self.sentences_two[4].text, "Some time after this the Bat was caught in just the \r\nsame way by another Weasel, and, as before, begged for its life.")
        self.assertEqual(self.sentences_two[5].text, "\"No,\" \r\nsaid the Weasel, \"I never let a mouse go by any chance.\"")
        self.assertEqual(self.sentences_two[6].text, "\"But I'm not \r\na mouse,\" said the Bat; \"I'm a bird.\"")
        self.assertEqual(self.sentences_two[7].text, "\"Why, so you are,\" said the \r\nWeasel; and he too let the Bat go. \r\n")

        self.assertEqual(self.sentences_three[0].text, "There was once a house that was overrun with Mice.")
        self.assertEqual(self.sentences_three[1].text, "A Cat heard of \r\nthis, and said to herself, \"That's the place for me,\" and off she went \r\nand took up her quarters in the house, and caught the Mice one by one \r\nand ate them.")
        self.assertEqual(self.sentences_three[2].text, "At last the Mice could stand it no longer, and they \r\ndetermined to take to their holes and stay there.")
        self.assertEqual(self.sentences_three[3].text, "\"That's awkward,\" \r\nsaid the Cat to herself: \"the only thing to do is to coax them out by \r\na trick.\"")
        self.assertEqual(self.sentences_three[4].text, "So she considered a while, and then climbed up the wall and \r\nlet herself hang down by her hind legs from a peg, and pretended to \r\nbe dead.")
        self.assertEqual(self.sentences_three[5].text, "By and by a Mouse peeped out and saw the Cat hanging there.")
        self.assertEqual(self.sentences_three[6].text, "\"Aha!\"")
        self.assertEqual(self.sentences_three[7].text, "it cried, \"you're very clever, madam, no doubt: but you may \r\nturn yourself into a bag of meal hanging there, if you like, yet you \r\nwon't catch us coming anywhere near you.\"")

    def test_IsBeginAndEndOfSentencesRight(self):
        self.assertEqual(self.sentences[0].begin, 0)
        self.assertEqual(self.sentences[0].end, 183)
        self.assertEqual(self.sentences[1].begin, 184)
        self.assertEqual(self.sentences[1].end, 404)
        self.assertEqual(self.sentences_two[0].begin, 0)
        self.assertEqual(self.sentences_two[0].end, 125)

    def test_AreEventsInRightSentence(self):
        # "saw" in first sentence
        self.assertIn(self.events[0], self.structure[self.sentences[0]])
        # "hanging" in first sentence
        self.assertIn(self.events[1], self.structure[self.sentences[0]])
        self.assertIn(self.events[2], self.structure[self.sentences[0]])
        self.assertIn(self.events[3], self.structure[self.sentences[0]])
        self.assertIn(self.events[4], self.structure[self.sentences[1]])
        self.assertIn(self.events[5], self.structure[self.sentences[1]])
        self.assertIn(self.events[6], self.structure[self.sentences[1]])
        self.assertIn(self.events[7], self.structure[self.sentences[1]])
        self.assertIn(self.events[8], self.structure[self.sentences[1]])

        self.assertIn(self.events_two[0], self.structure_two[self.sentences_two[0]])
        self.assertIn(self.events_two[1], self.structure_two[self.sentences_two[0]])
        self.assertIn(self.events_two[2], self.structure_two[self.sentences_two[0]])
        self.assertIn(self.events_two[3], self.structure_two[self.sentences_two[0]])
        self.assertIn(self.events_two[4], self.structure_two[self.sentences_two[1]])
        self.assertIn(self.events_two[5], self.structure_two[self.sentences_two[1]])
        self.assertIn(self.events_two[6], self.structure_two[self.sentences_two[2]])

        self.assertIn(self.events_three[0], self.structure_three[self.sentences_three[0]])
        self.assertIn(self.events_three[1], self.structure_three[self.sentences_three[1]])
        self.assertIn(self.events_three[2], self.structure_three[self.sentences_three[1]])
        self.assertIn(self.events_three[3], self.structure_three[self.sentences_three[1]])
        self.assertIn(self.events_three[4], self.structure_three[self.sentences_three[1]])
        self.assertIn(self.events_three[5], self.structure_three[self.sentences_three[1]])
        self.assertIn(self.events_three[6], self.structure_three[self.sentences_three[1]])
        self.assertIn(self.events_three[7], self.structure_three[self.sentences_three[2]])
        self.assertIn(self.events_three[8], self.structure_three[self.sentences_three[3]])
        self.assertIn(self.events_three[9], self.structure_three[self.sentences_three[4]])
        self.assertIn(self.events_three[10], self.structure_three[self.sentences_three[4]])
        self.assertIn(self.events_three[11], self.structure_three[self.sentences_three[4]])
        self.assertIn(self.events_three[12], self.structure_three[self.sentences_three[4]])
        self.assertIn(self.events_three[13], self.structure_three[self.sentences_three[5]])
        self.assertIn(self.events_three[14], self.structure_three[self.sentences_three[5]])
        self.assertIn(self.events_three[15], self.structure_three[self.sentences_three[5]])
        self.assertIn(self.events_three[16], self.structure_three[self.sentences_three[7]])

if __name__ == '__main__':
    unittest.main()
