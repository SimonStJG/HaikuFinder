# -*- coding: utf-8 -*-
import logging
import unittest


from haikufinder.finder import HaikuFinder, Word

HAIKU = "Greedy yellow birds. Sing the muddy riverbank. On a window sill."
HAIKU_WITHOUT_ENDING_PUNCTUATION = \
    "Greedy yellow birds. Sing the muddy riverbank. On a window sill"
HAIKU_WITH_NONSTANDARD_SPACING = \
    "Greedy yellow birds.  Sing the muddy riverbank.  On a window sill."
SEVEN_SYLLABLE_SENTENCE = "This is a random sentence. "
FIVE_SYLLABLE_SENTENCE = "Refrigerator."
UNKNOWN_WORD = "thisIsNotAWord. "


logger = logging.getLogger(__name__)


class TestHaikuFinder(unittest.TestCase):
    def setUp(self):
        self.haiku_finder = HaikuFinder()

    def test_paragraphs(self):
        self.assertEqual(
            self.haiku_finder.find_haiku("{}\n{}".format(HAIKU, HAIKU)),
            [HAIKU] * 2)

    def test_no_haiku(self):
        self.assertEqual(self.haiku_finder.find_haiku(
            SEVEN_SYLLABLE_SENTENCE + UNKNOWN_WORD),
            [])

    def test_finds_haiku(self):
        self.assertEqual(self.haiku_finder.find_haiku(HAIKU),
                         [HAIKU])

    def test_finds_three_haikus(self):
        self.assertEqual(
            self.haiku_finder.find_haiku(
                HAIKU + SEVEN_SYLLABLE_SENTENCE +
                FIVE_SYLLABLE_SENTENCE +
                UNKNOWN_WORD + HAIKU),
            [HAIKU,
             "On a window sill. " +
             SEVEN_SYLLABLE_SENTENCE +
             FIVE_SYLLABLE_SENTENCE,
             HAIKU])

    def test_finds_haiku_without_ending_punctuation(self):
        self.assertEqual(
            self.haiku_finder.find_haiku(HAIKU_WITHOUT_ENDING_PUNCTUATION),
            [HAIKU_WITHOUT_ENDING_PUNCTUATION])

    def test_unknown_word_is_ignored_at_beginning(self):
        self.assertEqual(
            self.haiku_finder.find_haiku(UNKNOWN_WORD + HAIKU),
            [HAIKU])

    def test_unknown_word_is_ignored_at_end(self):
        self.assertEqual(
            self.haiku_finder.find_haiku(HAIKU + UNKNOWN_WORD),
            [HAIKU])

    def test_unknown_word_triggers_callback(self):
        self.argument_captor = []

        def callback(word):
            logger.debug("Captured")
            self.argument_captor += [word]

        haiku_finder = HaikuFinder(custom_dictionary=None,
                                   unknown_word_callback=callback)
        haiku_finder.find_haiku("unknownword")
        self.assertEqual(self.argument_captor, ["unknownword"])

    def test_custom_dictionary(self):
        custom_dictionary = {"customword": 6}
        self.assertEqual(
            Word("customword",
                 {"custom_dictionary": custom_dictionary}).syllables,
            6)

    def test_hyphenation(self):
        self.assertEqual(Word("boom-box").syllables, 2)
