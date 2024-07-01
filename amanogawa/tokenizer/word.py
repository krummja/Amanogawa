from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from sudachipy import Morpheme
from enum import StrEnum, Enum, auto
from pygtrie import Trie
from amanogawa.tokenizer.util import katakana_to_hiragana


class Category(Enum):

    def __str__(self) -> str:
        return self.name

    ADJECTIVAL_NOUN = auto()
    ADJECTIVE = auto()
    ADVERB = auto()
    AUXILIARY_VERB = auto()
    CONJUNCTION = auto()
    COUNTER = auto()
    INTERJECTION = auto()
    NAME = auto()
    NOUN = auto()
    NUMBER = auto()
    PARTICLE = auto()
    PLACE_NAME = auto()
    PREFIX = auto()
    PRE_NOUN_ADJECTIVAL = auto()
    PRONOUN = auto()
    SUFFIX = auto()
    SYMBOL = auto()
    UNKNOWN = auto()
    VERB = auto()
    WHITESPACE = auto()


CATEGORY_MAPPING = Trie([
    # だいめいし
    (["代名詞"], Category.PRONOUN),

    # ふくし
    (["副詞"], Category.ADVERB),

    # じょどうし (lit. "particle-verb")
    (["助動詞"], Category.AUXILIARY_VERB),

    # じょし
    (["助詞"], Category.PARTICLE),

    # どうし
    (["動詞"], Category.VERB),

    # めいし (i.e. "naming word", nominal)
    (["名詞"], Category.NOUN),

    # めいし, こゆうめいし, じんめい
    (["名詞", "固有名詞", "人名"], Category.NAME),

    # めいし, こゆうめいし, ちめい
    (["名詞", "固有名詞", "地名"], Category.PLACE_NAME),

    # めいし, すうし
    (["名詞", "数詞"], Category.NUMBER),

    # めいし, ふつうめいし, じょすうしかのう
    (["名詞", "普通名詞", "助数詞可能"], Category.COUNTER),

    # けいようし
    (["形容詞"], Category.ADJECTIVE),

    # けいじょうし
    (["形状詞"], Category.ADJECTIVAL_NOUN),

    # かんどうし
    (["感動詞"], Category.INTERJECTION),

    # せつびじ
    (["接尾辞"], Category.SUFFIX),

    # せつびじ, めいしてき, じょすうし
    (["接尾辞", "名詞的", "助数詞"], Category.COUNTER),

    # せつぞくし
    (["接続詞"], Category.CONJUNCTION),

    # せっとうじ
    (["接頭辞"], Category.PREFIX),

    # くうはく
    (["空白"], Category.WHITESPACE),

    # ほじょきごう
    (["補助記号"], Category.SYMBOL),

    # きごう
    (["記号"], Category.SYMBOL),

    # れんたいし
    (["連体詞"], Category.PRE_NOUN_ADJECTIVAL),
])


class MorphemeInfo:

    def __init__(self, lexeme: str, morpheme: Morpheme) -> None:
        self._lexeme = lexeme
        self._morpheme = morpheme

        self.dictionary_form = self._morpheme.dictionary_form()
        self.normalized_form = self._morpheme.normalized_form()
        self.surface_form = self._morpheme.surface()
        self.reading_form = self._morpheme.reading_form()
        self.pos_info = self._morpheme.part_of_speech()
        self.start_idx = self._morpheme.begin()
        self.end_idx = self._morpheme.end()

    def pretty(self) -> dict[str, str]:
        return {
            "dictionary": self.dictionary_form,
            "normalized": self.normalized_form,
            "surface": self.surface_form,
            "reading": self.reading_form,
        }


class Word:

    def __init__(self, morphemes: list[Morpheme], form_reading: str  = "") -> None:
        self._morphemes = morphemes
        self._morpheme_info = [MorphemeInfo(form_reading, mm) for mm in morphemes]
        self._form_reading = form_reading

    @property
    def morphemes(self) -> list[Morpheme]:
        """The morphemes that make up the word."""
        return self._morphemes

    @property
    def surface(self) -> str:
        """The surface representation of the word."""
        return "".join(m.surface() for m in self._morphemes)

    @property
    def surface_reading(self) -> str:
        """The kana reading of the surface representation."""
        return katakana_to_hiragana("".join(m.reading_form() for m in self._morphemes))

    @property
    def dictionary_form(self) -> str:
        """The dictionary form of the word."""
        return self._morphemes[0].dictionary_form() if self._morphemes else ""

    @property
    def category(self) -> Category:
        """
        The lexical category of the word.

        We use a trie structure to map the morpheme features from the UniDic tags instead
        of a simple dict since there are feature tuples that can be mapped to more
        specific tags based on the longest matching prefix.
        """
        key = self._morphemes[0].part_of_speech()[:6]
        return CATEGORY_MAPPING.longest_prefix(key).value or Category.UNKNOWN

    def __iter__(self) -> Iterator[Morpheme]:
        yield from self._morphemes
