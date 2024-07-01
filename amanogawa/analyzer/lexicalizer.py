from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from amanogawa.analyzer.analyzer import Morpheme

import devtools as dev
import sudachipy as su
from enum import StrEnum
from amanogawa.analyzer.util import katakana_to_hiragana


class VerbCat(StrEnum):
    UNSPECIFIED = "Unspecified"
    MONOGRADE = "Monograde"
    BIGRADE = "Bigrade"
    QUADRIGRADE = "Quadrigrade"
    PENTAGRADE = "Pentagrade"
    IRREGULAR = "Irregular"


class MonoSubcat(StrEnum):
    UPPER = "Upper"
    LOWER = "Lower"


class Form(StrEnum):
    UNSPECIFIED = "Unspecified"
    IZENKEI = "Izenkei (Realis)"
    MIZENKEI = "Mizenkei (Irrealis)"
    KATEIKEI = "Kateikei (Conditional)"
    MEIREIKEI = "Meireikei (Imperative)"
    SHUUSHIKEI = "Shuushikei (Conclusive)"
    RENYOUKEI = "Renyoukei (Adverbial)"
    RENTAIKEI = "Rentaikei (Attributive)"


class Subform(StrEnum):
    UNSPECIFIED = "Unspecified"
    GENERAL = "General"
    SOKUONBIN = "Sokuonbin"


class PentaSubcat(StrEnum):
    pass


class Auxiliary(StrEnum):
    UNSPECIFIED = "Unspecified"
    CAUSATIVE = "Causative"
    PASSIVE = "Passive"
    NEGATION = "Negation"
    DESIDIRATIVE = "Desidirative"
    PERFECTIVE = "Perfective"
    HONORIFIC = "Honorific"


class Adjective(StrEnum):
    UNSPECIFIED = "Unspecified"
    NEGATION = "Negation"


class Word:

    def __init__(self, morphology: list[Morpheme]) -> None:
        self._morphemes = morphology

    @property
    def morphemes(self) -> list[Morpheme]:
        """The morphemes that make up the word."""
        return self._morphemes

    @property
    def surface(self) -> str:
        """The surface representation of the word."""
        return "".join(m.surface_form for m in self._morphemes)

    @property
    def surface_reading(self) -> str:
        """The kana reading of the surface representation."""
        return katakana_to_hiragana("".join(m.reading_form for m in self._morphemes))

    @property
    def dictionary_form(self) -> str:
        """The dictionary form of the word."""
        return self._morphemes[0].dictionary_form if self._morphemes else ""


class Constituent:

    def __init__(self, words: list[Word]) -> None:
        self._words = words


class Lexicalizer:

    def __init__(self, morphology: list[Morpheme]) -> None:
        self._morphology = morphology

    def lexicalize(self) -> list[Word]:
        self._categorize(self._morphology)
        return []

    def _categorize(self, morphology: list[Morpheme]):
        """
        Categorizes the morphology making up a word based on the UniDic categorization
        info provided by Sudachi. As an example, take the desidirative suffix -たい:

        ('助動詞', '*', '*', '*', '助動詞-タイ', '終止形-一般')
         AUXILIARY -------------- AUXILIARY-TAI SHUUSHIKEI-GENERAL

        We can thus categorize the suffix as a verbal auxiliary expressing the
        desidirative aspect in the "shuushikei" or ending form.
        """
        for morpheme in list(morphology):
            print(morpheme.dictionary_form, morpheme.category_info)
            match morpheme.category_info:
                case ["動詞", *rest]:
                    pass
                case ["助動詞", *rest]:
                    category = self._categorize_auxiliary(morpheme.dictionary_form, rest)
                    print(morpheme.dictionary_form, category)
                case ["形容詞", *rest]:
                    category = self._categorize_adjective(morpheme.dictionary_form, rest)
                    print(morpheme.dictionary_form, category)
                case _:
                    pass

    def _categorize_verb(self, category_info: list[str]):
        dev.debug(category_info)

    def _categorize_auxiliary(
        self,
        auxiliary: str,
        category_info: list[str],
    ) -> tuple[Auxiliary, Form, Subform]:
        match auxiliary, category_info:
            case _, [*_, "助動詞-レル", form]:
                return Auxiliary.PASSIVE, *self._match_form(form)
            case _, [*_, "助動詞-タイ", form]:
                return Auxiliary.DESIDIRATIVE, *self._match_form(form)
            case _, [*_, "助動詞-タ", form]:
                return Auxiliary.PERFECTIVE, *self._match_form(form)
            case "させる", [*_, form]:
                return Auxiliary.CAUSATIVE, *self._match_form(form)
            case _, [*_, "助動詞-マス", form]:
                return Auxiliary.HONORIFIC, *self._match_form(form)
            case _:
                return Auxiliary.UNSPECIFIED, Form.UNSPECIFIED, Subform.UNSPECIFIED

    def _categorize_adjective(self, adjective: str, category_info: list[str]):
        match adjective, category_info:
            case "ない", [*_, "形容詞", form]:
                return Adjective.NEGATION, self._match_form(form)

    def _match_form(self, form: str) -> tuple[Form, Subform]:
        match form.split("-"):
            case ["未然形", subform]:
                return Form.MIZENKEI, self._match_subform(subform)
            case ["連用形", subform]:
                return Form.RENYOUKEI, self._match_subform(subform)
            case ["終止形", subform]:
                return Form.SHUUSHIKEI, self._match_subform(subform)
            case _:
                return Form.UNSPECIFIED, Subform.UNSPECIFIED

    def _match_subform(self, subform: str) -> Subform:
        match subform:
            case "促音便":
                return Subform.SOKUONBIN
            case "一般":
                return Subform.GENERAL
            case _:
                return Subform.UNSPECIFIED
