from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from enum import StrEnum

import sudachipy as su
import devtools as dev
from nltk.tree import Tree, ParentedTree as PT
from nltk.featstruct import FeatStruct, FeatList, FeatDict, Variable
from nltk.grammar import Production, FeatureGrammar
from nltk.parse import generate, util
from nltk import parse

from amanogawa.categories import CATEGORIES_EN_JP
from amanogawa.categories import CATEGORIES_JP_EN
from amanogawa.categories import CONJUGATION_FORMS_EN_JP
from amanogawa.categories import CONJUGATION_FORMS_JP_EN
from amanogawa.categories import CONJUGATION_TYPES_EN_JP
from amanogawa.categories import CONJUGATION_TYPES_JP_EN
from amanogawa.database import retrieve_root
from amanogawa.morphology import MorphemeInfo
from amanogawa.analyzer.util import katakana_to_hiragana


class VerbClass(StrEnum):
    PENTAGRADE = "五段"
    UPPER_MONOGRADE = "上一段"
    LOWER_MONOGRADE = "下一段"
    IRREGULAR = "変"
    AUXILIARY = "助動詞"


class InflectionBase(StrEnum):
    MIZENKEI = "IRREALIS"
    RENYOUKEI = "CONTINUATIVE"
    SHUUSHIKEI = "CONCLUSIVE"
    RENTAIKEI = "ADNOMINAL"
    KATEIKEI = "HYPOTHETICAL"
    MEIREIKEI = "IMPERATIVE"
    IZENKEI = "PERFECTIVE"


GODAN_VERBS = [
    "会う",
    "歩く",
    "急ぐ",
    "話す",
    "待つ",
    "死ぬ",
    "学ぶ",
    "読む",
    "分かる",
    "切る",
    "売る",
    "帰る",
    "怒る",
]

ICHIDAN_VERBS = [
    "見る",
    "伸びる",
    "食べる",
]

HANASU = "話す"
OYOGU = "泳ぐ"
YORU = "寄る"
MIRU = "見る"


class StemRow(StrEnum):
    A_ROW = "ア"
    KA_ROW = "カ"
    GA_ROW = "ガ"
    SA_ROW = "サ"
    ZA_ROW = "ザ"
    TA_ROW = "タ"
    DA_ROW = "ダ"
    NA_ROW = "ナ"
    HA_ROW = "ハ"
    BA_ROW = "バ"
    MA_ROW = "マ"
    RA_ROW = "ラ"
    WAA_ROW = "ワア"


class VerbCategory(NamedTuple):
    verb_class: VerbClass
    stem_row: StemRow


VERB_CATEGORY_MAPPING = {
    "Ka row irregular case": VerbCategory(VerbClass.IRREGULAR, StemRow.KA_ROW),
    "Sa row irregular case": VerbCategory(VerbClass.IRREGULAR, StemRow.SA_ROW),

    "Kami Ichidan - A row": VerbCategory(VerbClass.UPPER_MONOGRADE, StemRow.A_ROW),
    "Kami Ichidan - Ka row": VerbCategory(VerbClass.UPPER_MONOGRADE, StemRow.KA_ROW),
    "Kami Ichidan - Ga row": VerbCategory(VerbClass.UPPER_MONOGRADE, StemRow.GA_ROW),
    "Kami Ichidan - Za row": VerbCategory(VerbClass.UPPER_MONOGRADE, StemRow.ZA_ROW),
    "Kami Ichidan - Ta row": VerbCategory(VerbClass.UPPER_MONOGRADE, StemRow.TA_ROW),
    "Kami Ichidan - Na row": VerbCategory(VerbClass.UPPER_MONOGRADE, StemRow.NA_ROW),
    "Kami Ichidan - Ha row": VerbCategory(VerbClass.UPPER_MONOGRADE, StemRow.HA_ROW),
    "Kami Ichidan - Ba row": VerbCategory(VerbClass.UPPER_MONOGRADE, StemRow.BA_ROW),
    "Kami Ichidan - Ma row": VerbCategory(VerbClass.UPPER_MONOGRADE, StemRow.MA_ROW),
    "Kami Ichidan - Ra row": VerbCategory(VerbClass.UPPER_MONOGRADE, StemRow.RA_ROW),

    "Shimo Ichidan - A row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.A_ROW),
    "Shimo Ichidan - Ka row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.KA_ROW),
    "Shimo Ichidan - Ga row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.GA_ROW),
    "Shimo Ichidan - Sa row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.SA_ROW),
    "Shimo Ichidan - Za row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.ZA_ROW),
    "Shimo Ichidan - Ta row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.TA_ROW),
    "Shimo Ichidan - Da row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.DA_ROW),
    "Shimo Ichidan - Na row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.NA_ROW),
    "Shimo Ichidan - Ha row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.HA_ROW),
    "Shimo Ichidan - Ba row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.BA_ROW),
    "Shimo Ichidan - Ma row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.MA_ROW),
    "Shimo Ichidan - Ra row": VerbCategory(VerbClass.LOWER_MONOGRADE, StemRow.RA_ROW),

    "Godan - Ka row": VerbCategory(VerbClass.PENTAGRADE, StemRow.KA_ROW),
    "Godan - Ga row": VerbCategory(VerbClass.PENTAGRADE, StemRow.GA_ROW),
    "Godan - Sa row": VerbCategory(VerbClass.PENTAGRADE, StemRow.SA_ROW),
    "Godan - Ta row": VerbCategory(VerbClass.PENTAGRADE, StemRow.TA_ROW),
    "Godan - Na row": VerbCategory(VerbClass.PENTAGRADE, StemRow.NA_ROW),
    "Godan - Ba row": VerbCategory(VerbClass.PENTAGRADE, StemRow.BA_ROW),
    "Godan - Ma row": VerbCategory(VerbClass.PENTAGRADE, StemRow.MA_ROW),
    "Godan - Ra row": VerbCategory(VerbClass.PENTAGRADE, StemRow.RA_ROW),
    "Godan - Waa row": VerbCategory(VerbClass.PENTAGRADE, StemRow.WAA_ROW),
}


class Verb:

    def __init__(self, base_form: str) -> None:
        self.base_form = base_form
        self.morphology_info: list[MorphemeInfo] = []
        self.inflections = {
            InflectionBase.MIZENKEI: "",
            InflectionBase.RENYOUKEI: "",
            InflectionBase.SHUUSHIKEI: "",
            InflectionBase.RENTAIKEI: "",
            InflectionBase.KATEIKEI: "",
            InflectionBase.MEIREIKEI: "",
            InflectionBase.IZENKEI: "",
        }

        self._build_morphology()
        self._build_inflections()

    def __getitem__(self, key: InflectionBase) -> str:
        return self.inflections[key]

    def _build_morphology(self) -> None:
        dictionary = su.Dictionary()
        tokenizer = dictionary.create()
        morphemes = tokenizer.tokenize(self.base_form)

        for morpheme in morphemes:
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

            self.morphology_info.append(info)

    def _build_inflections(self) -> None:
        root_morpheme = self.morphology_info[0]

        if root_morpheme.conjugation_type is None:
            raise ValueError("Missing conjugation type of verb stem.")
        if root_morpheme.reading_form is None:
            raise ValueError("Missing reading for of verb stem.")

        dictionary_form = root_morpheme.dictionary_form
        verb_category = VERB_CATEGORY_MAPPING[root_morpheme.conjugation_type]

        match verb_category[0]:
            case VerbClass.PENTAGRADE:
                self._inflect_godan(dictionary_form)
            case VerbClass.UPPER_MONOGRADE:
                self._inflect_ichidan(dictionary_form)
            case VerbClass.LOWER_MONOGRADE:
                self._inflect_ichidan(dictionary_form)
            case VerbClass.IRREGULAR:
                self._inflect_irregular(dictionary_form)

    def _inflect_ichidan(self, dictionary_form: str) -> None:
        stem = dictionary_form[0:-1]
        self.inflections[InflectionBase.MIZENKEI] = stem
        self.inflections[InflectionBase.RENYOUKEI] = stem
        self.inflections[InflectionBase.SHUUSHIKEI] = stem + "る"
        self.inflections[InflectionBase.RENTAIKEI] = stem + "る"
        self.inflections[InflectionBase.KATEIKEI] = stem + "れ"
        self.inflections[InflectionBase.MEIREIKEI] = stem + "よ"
        self.inflections[InflectionBase.IZENKEI] = stem + "れ"

    def _inflect_godan(self, dictionary_form: str) -> None:
        pass

    def _inflect_irregular(self, dictionary_form: str) -> None:
        pass


class Auxiliary:

    def __init__(self, base_form: str, selection: InflectionBase) -> None:
        self.base_form = base_form
        self.selection = selection

    def inflect(self, verb: Verb) -> str:
        return verb.inflections[self.selection] + self.base_form



def main() -> None:
    tabe = Verb("食べる")
    ta = Auxiliary("た", InflectionBase.RENYOUKEI)
    tabeta = ta.inflect(tabe)

    dev.debug(tabe.base_form)
    dev.debug(ta.base_form)
    dev.debug(tabeta)


if __name__ == '__main__':
    main()
