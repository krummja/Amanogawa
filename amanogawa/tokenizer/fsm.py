from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from sudachipy import Morpheme

import devtools as dev

from amanogawa.tokenizer.exceptions import StateNotFoundException


class State(Protocol):

    def on_input(self, context: Any, morpheme: Morpheme) -> None:
        """Process the current input."""
        ...


MorphemeFeatures: TypeAlias = tuple[str, str, str, str]

StateTransitionRule: TypeAlias = tuple[State | None, MorphemeFeatures, State]


def get_morpheme_features(morpheme: Morpheme) -> MorphemeFeatures:
    category = morpheme.part_of_speech()
    return category[0], category[1], category[2], category[3]


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

    def get_next_state(self, source_state: State, morpheme: Morpheme) -> State:
        features = get_morpheme_features(morpheme)

        if (source_state, features) in self._transitions:
            return self._transitions[(source_state, features)]
        elif (None, features) in self._transitions:
            return self._transitions[(None, features)]
        return self._default_state

    def run(self, context: Any, morphemes: Iterable[Morpheme]) -> Any:
        current_state = self._initial_state

        for morpheme in morphemes:
            next_state = self.get_next_state(current_state, morpheme)
            next_state.on_input(context, morpheme)
            current_state = next_state

        return context
