from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from sudachipy import Morpheme

import devtools as dev

from amanogawa.tokenizer.exceptions import StateNotFoundException


class State(Protocol):

    name: str

    def on_input(self, context: Any, morpheme: Morpheme) -> None:
        """Process the current input."""


MorphemeFeatures: TypeAlias = tuple[str, ...]
StateTransitionRule: TypeAlias = tuple[State | None, MorphemeFeatures, State]


def get_morpheme_features(morpheme: Morpheme, size: int = 4) -> MorphemeFeatures:
    category = morpheme.part_of_speech()
    return tuple(category[:size])


class StateMachine:

    def __init__(
        self,
        states: list[State],
        initial_state: State,
        default_state: State,
        transitions: list[StateTransitionRule],
    ) -> None:
        self._states = frozenset(states)
        self._transitions = {}

        if initial_state not in self._states:
            raise StateNotFoundException()
        if default_state not in self._states:
            raise StateNotFoundException()

        self._initial_state = initial_state
        self._default_state = default_state

        for src, features, dst in transitions:
            self._transitions[(src, features)] = dst

    def get_next_state(self, source_state: State, morpheme: Morpheme, size: int) -> State:
        features = get_morpheme_features(morpheme, size)
        if (source_state, features) in self._transitions:
            return self._transitions[(source_state, features)]
        elif (None, features) in self._transitions:
            return self._transitions[(None, features)]
        return self._default_state

    def run(self, context: Any, morphemes: Iterable[Morpheme]) -> Any:
        current_state = self._initial_state

        for morpheme in morphemes:
            first_pass = self.get_next_state(current_state, morpheme, 4)
            first_pass.on_input(context, morpheme)
            current_state = first_pass

            second_pass = self.get_next_state(current_state, morpheme, 6)
            second_pass.on_input(context, morpheme)
            dev.debug(first_pass.name)
            dev.debug(second_pass.name)

        return context
