from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import nltk
from nltk import Production, Tree


Token: TypeAlias = str
Backtrack: TypeAlias = Literal[True]
ParserResult: TypeAlias = Backtrack | Token | Production | None
Frontier: TypeAlias = list[tuple[int]]


class Parser:

    def __init__(self, grammar: nltk.grammar.CFG) -> None:
        self.grammar = grammar
        self._parser = nltk.parse.SteppingRecursiveDescentParser(self.grammar)
        self._parses = []

    @property
    def parses(self) -> list[Tree]:
        return list(self._parses)

    @property
    def remainder(self) -> list[str]:
        return cast(list[str], self._parser.remaining_text)

    @property
    def untried(self) -> list[Production]:
        return self._parser.untried_expandable_productions()

    @property
    def tree(self) -> Tree | None:
        return self._parser.tree()

    @property
    def history(self) -> list[tuple[str, Tree, Frontier]]:
        return self._parser._history

    def initialize(self, tokens: list[str]) -> None:
        self._parser.initialize(tokens)

    def parse(self, depth: int = 100) -> Iterator[ParserResult]:
        for _ in range(depth):
            step_result = self._parser.step()
            if self._parser.currently_complete():
                self._parses.append(self.tree)
            if not step_result:
                break
            yield step_result
