# -*- coding: utf-8 -*-
import unittest

from haikufinder.finder import find_haiku, Word

HAIKU = "Greedy yellow birds. Sing the muddy riverbank. On a window sill."
HAIKU_WITHOUT_ENDING_PUNCTUATION = \
    "Greedy yellow birds. Sing the muddy riverbank. On a window sill"
HAIKU_WITH_NONSTANDARD_SPACING = \
    "Greedy yellow birds.  Sing the muddy riverbank.  On a window sill."
SEVEN_SYLLABLE_SENTENCE = "This is a random sentence. "
FIVE_SYLLABLE_SENTENCE = "Refrigerator."
UNKNOWN_WORD = "thisIsNotAWord. "


class TestHaikuFinder(unittest.TestCase):
    def test_no_haiku(self):
        self.assertEqual(find_haiku(SEVEN_SYLLABLE_SENTENCE + UNKNOWN_WORD),
                         [])

    def test_finds_haiku(self):
        self.assertEqual(find_haiku(HAIKU), [HAIKU])

    def test_finds_three_haikus(self):
        self.assertEqual(find_haiku(HAIKU + SEVEN_SYLLABLE_SENTENCE +
                                    FIVE_SYLLABLE_SENTENCE +
                                    UNKNOWN_WORD + HAIKU),
                         [HAIKU,
                          "On a window sill. " +
                          SEVEN_SYLLABLE_SENTENCE +
                          FIVE_SYLLABLE_SENTENCE,
                          HAIKU])

    def test_finds_haiku_without_ending_punctuation(self):
        self.assertEqual(find_haiku(HAIKU_WITHOUT_ENDING_PUNCTUATION),
                         [HAIKU_WITHOUT_ENDING_PUNCTUATION])

    def test_unknown_word_is_ignored_at_beginning(self):
        self.assertEqual(
            find_haiku(UNKNOWN_WORD + HAIKU),
            [HAIKU])

    def test_unknown_word_is_ignored_at_end(self):
        self.assertEqual(
            find_haiku(HAIKU + UNKNOWN_WORD),
            [HAIKU])

    def test_hyphenation(self):
        self.assertEqual(Word("boom-box").syllables, 2)
