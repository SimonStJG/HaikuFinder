# -*- coding: utf-8 -*-
"""
Public Classes:
 * HaikuFinder
"""
import nltk
import logging
from functools import reduce
from cached_property import cached_property

logger = logging.getLogger(__name__)

try:
    cmu_dictionary = nltk.corpus.cmudict.dict()
except LookupError:
    if not nltk.download("cmudict"):
        raise Exception("Failed to download cmudict")
    cmu_dictionary = nltk.corpus.cmudict.dict()

PUNCTUATION = [".", "!", "(", ")", ":", ",", "?", ";"]


class HaikuFinder(object):
    def __init__(self, custom_dictionary=None, unknown_word_callback=None):
        self.config = {"custom_dictionary": custom_dictionary,
                       "unknown_word_callback": unknown_word_callback}

    def find_haiku(self, text):
        """
        Find a list of Haiku in text.
        :param text: The text to search
        :return: List of found haiku
        """
        return flatten([Paragraph(paragraph, self.config).find_haiku()
                        for paragraph in text.split("\n")])


class Paragraph(object):
    def __init__(self, text, config):
        self._config = config
        self._clauses = self.split_into_clauses(text)

    def split_into_clauses(self, paragraph):
        clauses = []
        next_clause_starting_position = 0
        for i, char in enumerate(paragraph):
            if char in PUNCTUATION:
                clause = paragraph[next_clause_starting_position:i].strip()
                if clause:
                    clauses.append(Clause(clause, char, self._config))
                next_clause_starting_position = i + 1

        final_clause = paragraph[next_clause_starting_position:].strip()
        if final_clause:
            clauses.append(Clause(final_clause, '', self._config))

        return clauses

    def find_haiku(self):
        logger.debug("Finding haiku in {}".format(self))
        haiku_found = []
        syllable_lengths = [x.syllables for x in self._clauses]
        for i in range(0, len(self._clauses) - 2):
            if syllable_lengths[i:i+3] == [5, 7, 5]:
                haiku_found.append(" ".join(
                    [x.full_text for x in self._clauses[i:i+3]]))

        return haiku_found

    def __repr__(self):
        return "Paragraph: ({})".format(", ".join(map(repr, self._clauses)))


class Clause(object):
    def __init__(self, text, ending_punctuation, config):
        self._config = config
        self._text = text
        self._ending_punctuation = ending_punctuation

    @cached_property
    def syllables(self):
        try:
            return sum([Word(word, self._config).syllables
                        for word in self._text.split()])
        except WordNotFoundException:
            return None

    @cached_property
    def full_text(self):
        return self._text + self._ending_punctuation

    def __repr__(self):
        return "Clause: {}({})".format(self.full_text, self.syllables)


class Word(object):
    def __init__(self, text, config=None):
        logger.debug("Creating word: {}".format(text))
        assert text is not None and text != ""
        self._custom_dictionary = \
            config.get("custom_dictionary") if config is not None else None
        self._unknown_word_callback = \
            config.get("unknown_word_callback") if config is not None else None
        self._text = text

    @cached_property
    def syllables(self):
        """Number of syllables in word.

        :raises WordNotFoundException: if the word wasn't found in the
        dictionary."""

        # If the word is hyphenated then use the sum of the word on each side
        # of the hyphen
        if "-" in self._text:
            return sum([Word(w).syllables for w in self._text.split("-")])

        try:
            # cmudict actually returns a list of phonetics, so by default
            # choose first length
            return len([1 for syllable in cmu_dictionary[self._text.lower()][0]
                        if is_vowel_sound(syllable)])

        except KeyError:
            if self._custom_dictionary and \
                    self._text.lower() in self._custom_dictionary:
                return self._custom_dictionary[self._text.lower()]
        if self._unknown_word_callback:
            self._unknown_word_callback(self._text)
        raise WordNotFoundException


def is_vowel_sound(syllable):
    return syllable[-1] in map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])


def flatten(list):
    return reduce(lambda x, xs: x + xs, list)


class WordNotFoundException(Exception):
    pass
