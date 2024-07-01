from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import devtools as dev
import sudachipy as su

from amanogawa.analyzer.util import katakana_to_hiragana
from amanogawa.analyzer.lexicalizer import Lexicalizer


class Morpheme:

    def __init__(self, morpheme: su.Morpheme) -> None:
        self._morpheme = morpheme

    @property
    def dictionary_form(self):
        """The dictionary headword form of the morpheme."""
        return self._morpheme.dictionary_form()

    @property
    def normalized_form(self):
        """The normalized form of the morpheme."""
        return self._morpheme.normalized_form()

    @property
    def surface_form(self):
        """The surface representation of the morpheme."""
        return self._morpheme.surface()

    @property
    def reading_form(self):
        """The hiragana reading of the surface representation."""
        return katakana_to_hiragana(self._morpheme.reading_form())

    @property
    def components(self) -> su.MorphemeList:
        """Returns the constituent sub-morphemes of this morpheme."""
        return self._morpheme.split(mode=su.SplitMode.A, add_single=True)

    @property
    def category_info(self):
        return self._morpheme.part_of_speech()


class Analyzer:

    def __init__(self) -> None:
        self._dictionary = su.Dictionary()
        self._tokenizer = self._dictionary.create()

    def find_form_reading(self, morpheme: su.Morpheme) -> str:
        """Retrieve the dictionary form for a given morpheme."""
        result = self._dictionary.lookup(morpheme.surface())[0]
        return katakana_to_hiragana(result.reading_form())

    def tokenize(self, phrase: str) -> su.MorphemeList:
        """Use the internal Sudachi tokenizer to tokenize the input phrase."""
        return self._tokenizer.tokenize(phrase)

    def lexicalize(self, morphemes: su.MorphemeList):
        """
        Build a morphology from the (Sudachi) `MorphemeList`, then create words from the
        morphological components. This allows us to be very fine-grained in how we break
        apart the input phrase into a set of lexical items for analysis.

        Additionally, we can provide useful lexical information for later phases of the
        analysis process.
        """
        morphology = [Morpheme(mm) for mm in morphemes]
        lexicon = Lexicalizer(morphology).lexicalize()


if __name__ == '__main__':
    analyzer = Analyzer()
    morphemes = analyzer.tokenize("食べさせられたくなかった")
    analyzer.lexicalize(morphemes)
