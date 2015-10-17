# -*- coding: utf-8 -*-
"""
Public Methods:
 * find_haiku
"""
import nltk
import logging
from functools import reduce

logger = logging.getLogger(__name__)
cmu_dictionary = nltk.corpus.cmudict.dict()
PUNCTUATION = [".", "!", "(", ")", ":", ",", "?", ";"]


def find_haiku(text):
    """
    Find a list of Haiku in text.
    :param text: The text to search
    :return: List of found haiku
    """
    return flatten([Paragraph(paragraph).find_haiku()
                    for paragraph in text.split("\n")])


def flatten(list):
    return reduce(lambda x, xs: x + xs, list)


class Paragraph(object):
    def __init__(self, text):
        self.clauses = self.split_into_clauses(text)

    @staticmethod
    def split_into_clauses(paragraph):
        clauses = []
        next_clause_starting_position = 0
        for i, char in enumerate(paragraph):
            if char in PUNCTUATION:
                clause = paragraph[next_clause_starting_position:i].strip()
                if clause:
                    clauses.append(Clause(clause, char))
                next_clause_starting_position = i + 1

        final_clause = paragraph[next_clause_starting_position:].strip()
        if final_clause:
            clauses.append(Clause(final_clause, ''))

        return clauses

    def find_haiku(self):
        logger.debug("Finding haiku in {}".format(self))
        haiku_found = []
        syllable_lengths = [x.syllables for x in self.clauses]
        for i in range(0, len(self.clauses) - 2):
            if syllable_lengths[i:i+3] == [5, 7, 5]:
                haiku_found.append(" ".join(
                    [x.full_text for x in self.clauses[i:i+3]]))

        return haiku_found

    def __repr__(self):
        return "Paragraph: ({})".format(", ".join(map(repr, self.clauses)))


class Clause(object):
    def __init__(self, text, ending_punctuation):
        self.text = text
        self.ending_punctuation = ending_punctuation

    @property
    def syllables(self):
        try:
            return sum([Word(word).syllables for word in self.text.split()])
        except WordNotFoundException:
            return None

    @property
    def full_text(self):
        return self.text + self.ending_punctuation

    def __repr__(self):
        return "Clause: {}({})".format(self.full_text, self.syllables)


class Word(object):
    def __init__(self, text):
        assert text is not None and text != ""
        self.text = text

    @property
    def syllables(self):
        """Number of syllables in word.

        :raises WordNotFoundException: if the word wasn't found in the
        dictionary."""

        # If the word is hypenated then use the sum of the word on each side of
        #  the hyphen
        if "-" in self.text:
            return sum([Word(w).syllables for w in self.text.split("-")])

        try:
            # cmudict actually returns a list of phonetics, so by default
            # choose first length
            return len([1 for syllable in cmu_dictionary[self.text.lower()][0]
                        if is_vowel_sound(syllable)])

        except KeyError:
            raise WordNotFoundException


def is_vowel_sound(syllable):
    return syllable[-1] in map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])


class WordNotFoundException(Exception):
    pass
