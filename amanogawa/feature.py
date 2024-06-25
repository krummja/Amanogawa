from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import devtools as dev
from enum import StrEnum
from nltk import grammar, parse
from nltk import FeatStruct, FeatStructReader, Variable
from nltk.grammar import FeatStructNonterminal, Production
from dango.word import PartOfSpeech


class Tense(StrEnum):
    PAST = "PAST"
    PRES = "PRES"
    FUT = "FUT"


def test():
    # start = FeatStructNonterminal("DP")
    # DP = Production("DP[AGR=?a]", ["D[AGR=?a]", "N[AGR=?a]"])
    # this = Production("D[AGR=[NUM='sg']]", ["this", "that"])
    # these = Production("N[AGR=[NUM='pl']]", ["these", "those"])
    # student = Production("N[AGR=[NUM='sg']]", ["student"])
    # students = Production("N[AGR=[NUM='pl']]", ["students"])
    # g = grammar.FeatureGrammar(start, [DP, this, these, student, students])

    rules = """
    % start DP
    DP[AGR=?a] -> D[AGR=?a] N[AGR=?a]
    D[AGR=[NUM='sg', PERS=3]] -> 'this' | 'that'
    D[AGR=[NUM='pl', PERS=3]] -> 'these' | 'those'
    D[AGR=[NUM='pl', PERS=1]] -> 'we'
    D[AGR=[PERS=2]] -> 'you'
    N[AGR=[NUM='sg', GND='m']] -> 'boy'
    N[AGR=[NUM='pl', GND='m']] -> 'boys'
    N[AGR=[NUM='sg', GND='f']] -> 'girl'
    N[AGR=[NUM='pl', GND='f']] -> 'girls'
    N[AGR=[NUM='sg']] -> 'student'
    N[AGR=[NUM='pl']] -> 'students'
    """

    PHI = FeatStruct(
        agr=FeatStruct(
            number=Variable("?n"),
            person=Variable("?p"),
            gender=Variable("?g"),
        ),
    )

    print(PHI)


if __name__ == '__main__':
    test()
