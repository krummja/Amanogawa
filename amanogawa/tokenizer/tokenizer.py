from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import devtools as dev

from sudachipy import Dictionary
from sudachipy.morpheme import Morpheme

from amanogawa.tokenizer.fsm import State
from amanogawa.tokenizer.fsm import StateMachine
from amanogawa.tokenizer.word import Word
from amanogawa.tokenizer.util import katakana_to_hiragana


class WordState(State):

    def __init__(self, name: str, start_new_word: bool = False) -> None:
        self.name = name
        self.start_new_word = start_new_word

    def on_input(self, context: list[list[Morpheme]], morpheme: Morpheme) -> None:
        if self.start_new_word:
            context.append([])
        context[-1].append(morpheme)


UNSPECIFIED_WORD_STATE = WordState("UNSPECIFIED", start_new_word=True)
VERB_STATE = WordState("VERB", start_new_word=True)
ADJECTIVE_STATE = WordState("ADJECTIVE", start_new_word=True)
VERB_INFLECTION_STATE = WordState("VERB_INFLECTION")
ADJECTIVE_INFLECTION_STATE = WordState("ADJECTIVE_INFLECTION")


WordAggregator = StateMachine(
    [
        UNSPECIFIED_WORD_STATE,
        VERB_STATE,
        VERB_INFLECTION_STATE,
        ADJECTIVE_STATE,
        ADJECTIVE_INFLECTION_STATE,
    ],
    UNSPECIFIED_WORD_STATE,
    UNSPECIFIED_WORD_STATE,
    [
        # --- transitions to aggregate inflected verbs ---

        # start of a verb
        (None, ('動詞', '一般', '*', '*'), VERB_STATE),

        # Some verbs (for example 見る) are detected as non-independent even when standing
        # alone, so we also need to account for these cases for starting a new verb.
        # Since specific transitions have higher priority than wildcard transition, we
        # don't risk breaking apart an inflected verb by accident.
        (None, ('動詞', '非自立可能', '*', '*'), VERB_STATE),

        # The inflected part of a verb is started by either an auxiliary verb, ...
        (VERB_STATE, ('助動詞', '*', '*', '*'), VERB_INFLECTION_STATE),

        # or a conjunctive particle, i.e. て or で.
        (VERB_STATE, ('助詞', '接続助詞', '*', '*'), VERB_INFLECTION_STATE),

        # continue aggregating any auxiliary verbs ...
        (VERB_INFLECTION_STATE, ('助動詞', '*', '*', '*'), VERB_INFLECTION_STATE),

        # and non independent verbs, e.g. the いる　of the continuous form
        (VERB_INFLECTION_STATE, ('動詞', '非自立可能', '*', '*'), VERB_INFLECTION_STATE),

        # suffix for seeming/looks-like
        (VERB_STATE, ('形状詞', '助動詞語幹', '*', '*'), VERB_INFLECTION_STATE),

        # --- transitions to aggregate inflected adjectives ---

        # start of an adjective
        (None, ('形容詞', '一般', '*', '*'), ADJECTIVE_STATE),

        # can be followed by negating suffix
        (ADJECTIVE_STATE, ('形容詞', '非自立可能', '*', '*'), ADJECTIVE_INFLECTION_STATE),

        # and/or suffix for the past-tense
        (ADJECTIVE_STATE, ('助動詞', '*', '*', '*'), VERB_INFLECTION_STATE),
        (ADJECTIVE_INFLECTION_STATE, ('助動詞', '*', '*', '*'), VERB_INFLECTION_STATE),

        # suffix for seeming/looks-like
        (ADJECTIVE_STATE, ('形状詞', '助動詞語幹', '*', '*'), ADJECTIVE_INFLECTION_STATE)
    ],
)


class Tokenizer:

    def __init__(self) -> None:
        self._dictionary = Dictionary()
        self._tokenizer = self._dictionary.create()

    def find_form_reading(self, morpheme: Morpheme) -> str:
        result = self._dictionary.lookup(morpheme.surface())[0]
        return katakana_to_hiragana(result.reading_form())

    def create_word(self, morphemes: list[Morpheme]) -> Word:
        return Word(morphemes, self.find_form_reading(morphemes[0]))

    def tokenize(self, phrase: str) -> list[Word]:
        morphemes = self._tokenizer.tokenize(phrase)
        return [self.create_word(mm) for mm in WordAggregator.run([], morphemes)]


if __name__ == '__main__':
    tokenizer = Tokenizer()
    result = tokenizer.tokenize("日本語で話す")

    for word in result:
        dev.debug(word.category)
        dev.debug(word.surface)
        dev.debug(word.surface_reading)
        dev.debug(word.dictionary_form)
