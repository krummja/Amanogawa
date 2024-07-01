from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import devtools as dev
from sudachipy import Morpheme
from sudachipy import Dictionary

from amanogawa.tokenizer.word import Word
from amanogawa.tokenizer.fsm import State
from amanogawa.tokenizer.fsm import StateMachine
from amanogawa.tokenizer.util import katakana_to_hiragana
from amanogawa.tokenizer.tokenizer import Tokenizer


class MorphemeState(State):

    def __init__(self, name: str) -> None:
        self.name = name

    def on_input(self, context: list[Morpheme], morpheme: Morpheme) -> None:
        context.append(morpheme)


UNSPECIFIED_MORPHEME_STATE = MorphemeState("UNSPECIFIED")
VERB_ROOT_STATE = MorphemeState("VERB_ROOT")
VERB_STEM_STATE = MorphemeState("VERB_STEM")
MASU_STATE = MorphemeState("MASU")
TENSE_INFLECTION_STATE = MorphemeState("TENSE_INFLECTION")


MorphemeAggregator = StateMachine(
    [
        UNSPECIFIED_MORPHEME_STATE,
        VERB_ROOT_STATE,
        VERB_STEM_STATE,
        MASU_STATE,
        TENSE_INFLECTION_STATE,
    ],
    UNSPECIFIED_MORPHEME_STATE,
    UNSPECIFIED_MORPHEME_STATE,
    [
        (
            None,
            ("動詞", "非自立可能", "*", "*"),
            VERB_ROOT_STATE,
        ),
        (
            None,
            ("動詞", "一般", "*", "*", "下一段-ア行", "連用形-一般"),
            VERB_STEM_STATE,
        ),
        (
            VERB_STEM_STATE,
            ("助動詞", "*", "*", "*", "助動詞-マス", "連用形-一般"),
            MASU_STATE,
        ),
        (
            MASU_STATE,
            ("助動詞", "*", "*", "*", "助動詞-タ", "終止形-一般"),
            TENSE_INFLECTION_STATE,
        )
    ]
)


class Morphology:

    def __init__(self, morphemes: list[Morpheme]) -> None:
        self._morphemes = morphemes


class Analyzer:

    def create_morphology(self, morphemes: list[Morpheme]) -> Morphology:
        return Morphology(morphemes)

    def parse(self, word: Word):
        aggregation: list[Morpheme] = MorphemeAggregator.run([], word.morphemes)
        for morpheme in aggregation:
            pass


if __name__ == "__main__":
    tokenizer = Tokenizer()
    analyzer = Analyzer()

    result = tokenizer.tokenize("見ました")
    for word in result:
        result = analyzer.parse(word)
