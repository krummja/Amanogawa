from __future__ import annotations
from typing import *

import nltk.parse.generate
if TYPE_CHECKING:
    pass

# import dango
import nltk
import rich
import devtools as dev
from dataclasses import dataclass, KW_ONLY
# from dango.word import PartOfSpeech
from enum import StrEnum
from nltk import grammar, parse
from nltk import FeatStruct, FeatStructReader, Variable
from nltk.grammar import FeatStructNonterminal, Production

from amanogawa.parser import Parser


# categories = {
#     "代名詞": PartOfSpeech.PRONOUN,
#     "名詞": PartOfSpeech.NOUN,
#     "助詞": PartOfSpeech.PARTICLE,
#     "動詞": PartOfSpeech.VERB,
#     "助動詞": PartOfSpeech.AUXILIARY_VERB,
#     "接尾辞": PartOfSpeech.SUFFIX,
#     "副詞": PartOfSpeech.ADVERB,
#     "形容詞": PartOfSpeech.ADJECTIVE,
# }


# @dataclass(kw_only=True)
# class Morpheme:
#     category: PartOfSpeech
#     surface_form: str
#     dictionary_form: str
#     normalized_form: str


# @dataclass(kw_only=True)
# class Lexeme:
#     category: PartOfSpeech
#     surface_form: str
#     surface_reading: str
#     dictionary_form: str
#     dictionary_reading: str
#     morphology: list[Morpheme]


# def dango_to_featstruct(item: Lexeme) -> FeatStruct:
#     return FeatStruct(
#         category=item.category,
#         spell_out=item.surface_form,
#     )


# def map_category(cat: list[str]) -> PartOfSpeech:
#     return categories[cat[0]]


def main() -> None:
    pass
    # words = dango.tokenize("私はリンゴを食べました")

    # lexicon = []

    # for word in words:
    #     for morpheme in word.morphemes:
    #         dev.debug(morpheme.part_of_speech())

    #     lexeme = Lexeme(
    #         category=word.part_of_speech,
    #         surface_form=word.surface,
    #         surface_reading=word.surface_reading,
    #         dictionary_form=word.dictionary_form,
    #         dictionary_reading=word.dictionary_form_reading,
    #         morphology=[
    #             Morpheme(
    #                 category=map_category(morph.part_of_speech()),
    #                 surface_form=morph.surface(),
    #                 dictionary_form=morph.dictionary_form(),
    #                 normalized_form=morph.normalized_form(),
    #             ) for morph in word.morphemes
    #         ],
    #     )

    #     lexicon.append(lexeme)

    # dev.debug(lexicon)


if __name__ == '__main__':
    main()
