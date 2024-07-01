from __future__ import annotations
from typing import *

from enum import StrEnum
import nltk
import rich
import devtools as dev
import sudachipy as su

from amanogawa.categories import CATEGORIES_EN_JP
from amanogawa.categories import CATEGORIES_JP_EN
from amanogawa.categories import CONJUGATION_FORMS_EN_JP
from amanogawa.categories import CONJUGATION_FORMS_JP_EN
from amanogawa.categories import CONJUGATION_TYPES_EN_JP
from amanogawa.categories import CONJUGATION_TYPES_JP_EN

from amanogawa.translation import translate
from amanogawa.translation import TranslationData
from amanogawa.tts import text_to_speech
from amanogawa.analyzer.util import katakana_to_hiragana
from amanogawa.morphology import MorphemeInfo


class Phrase:

    def __init__(
        self,
        original_text: str,
        morphemes: su.MorphemeList,
        translation: str,
    ) -> None:
        self.original_text = original_text
        self.morphemes = morphemes
        self.translation = translation

    @property
    def morphology(self) -> list[MorphemeInfo]:
        morphemes = []
        for morpheme in self.morphemes:
            raw_pos = morpheme.part_of_speech()
            info = MorphemeInfo(
                dictionary_form=morpheme.dictionary_form(),
                surface_form=morpheme.surface(),
                reading_form=katakana_to_hiragana(morpheme.reading_form()),
                category_0=CATEGORIES_JP_EN[raw_pos[0]],
                category_1=CATEGORIES_JP_EN[raw_pos[1]],
                category_2=CATEGORIES_JP_EN[raw_pos[2]],
                category_3=CATEGORIES_JP_EN[raw_pos[3]],
                conjugation_type=CONJUGATION_TYPES_JP_EN[raw_pos[4]],
                conjugation_form=CONJUGATION_FORMS_JP_EN[raw_pos[5]],
            )

            morphemes.append(info)
        return morphemes

    def __iter__(self) -> Iterator[MorphemeInfo]:
        yield from self.morphology


class Word:

    def __init__(self, original_text: str, morphemes: su.MorphemeList) -> None:
        self.original_text = original_text
        self.morphemes = morphemes

    @property
    def morphology(self) -> list[MorphemeInfo]:
        morphemes = []
        for morpheme in self.morphemes:
            raw_pos = morpheme.part_of_speech()
            dev.debug(morpheme.word_id())
            info = MorphemeInfo(
                dictionary_form=morpheme.dictionary_form(),
                surface_form=morpheme.surface(),
                reading_form=katakana_to_hiragana(morpheme.reading_form()),
                category_0=CATEGORIES_JP_EN[raw_pos[0]],
                category_1=CATEGORIES_JP_EN[raw_pos[1]],
                category_2=CATEGORIES_JP_EN[raw_pos[2]],
                category_3=CATEGORIES_JP_EN[raw_pos[3]],
                conjugation_type=CONJUGATION_TYPES_JP_EN[raw_pos[4]],
                conjugation_form=CONJUGATION_FORMS_JP_EN[raw_pos[5]],
            )

            morphemes.append(info)
        return morphemes

    @property
    def translation(self) -> TranslationData:
        return translate(self.original_text)

    @property
    def forms(self) -> list[tuple[str, str]]:
        forms = []
        for morpheme in self.morphology:
            forms.append([morpheme.dictionary_form, morpheme.conjugation_form])
        return forms

    def __iter__(self) -> Iterator[MorphemeInfo]:
        yield from self.morphology

    def __str__(self) -> str:
        morphemes = []
        for morpheme in self.morphemes:
            morphemes.append(morpheme.surface())
        morpheme_str = "・".join(morphemes)
        return f"{self.original_text} [{morpheme_str}]"


def main() -> None:
    dictionary = su.Dictionary(dict="full")
    tokenizer = dictionary.create()

    text = "大人らしくするつもりだったのに、大騒ぎしてしまった"
    text2 = "彼女がきれいなのに彼氏がいません"
    result = tokenizer.tokenize(text)
    word = Word(text, result)

    for morpheme in word.morphology:
        print(morpheme)

    # translated = translate(text)
    # translation = translated["translatedText"]
    # phrase = Phrase(text, result, translation)

    # dev.debug(phrase.translation)
    # dev.debug(phrase.morphology)

    # text_to_speech(text, "sentence")
    # for i, morpheme in enumerate(phrase):
    #     text_to_speech(str(morpheme.surface_form), f"morpheme_{str(i)}")


if __name__ == '__main__':
    main()
