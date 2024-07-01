from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pendulum as pdl
import polars as pl
import devtools as dev
from enum import StrEnum
from sqlalchemy import create_engine
from sqlalchemy import Engine
from contextlib import contextmanager

from amanogawa.config import DB_USER
from amanogawa.config import DB_PASS
from amanogawa.config import DB_DATABASE


class CategoryQuery(StrEnum):
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    COUNTER = "counter"
    CONJUNCTION = "conjunction"
    PARTICLE = "particle"
    NUMERIC = "numeric"
    AUXILIARY = "auxiliary"
    EXPRESSION = "expression"
    UNCLASSIFIED = "unclassified"
    COPULA = "copula"


class VerbCategory(StrEnum):
    TRANSITIVE = "transitive"
    INTRANSITIVE = "intransitive"
    GODAN = "godan"
    NIDAN = "nidan"
    ICHIDAN = "ichidan"
    YODAN = "yodan"
    SURU = "suru"


class NounCategory(StrEnum):
    COMMON = "common"
    PREFIX = "prefix"


@contextmanager
def initialize_engine(echo: bool = False) -> Iterator[Engine]:
    protocol = "postgresql+psycopg2://"
    URI = f"{protocol}{DB_USER}:{DB_PASS}@127.0.0.1:5432/{DB_DATABASE}"
    engine = create_engine(url=URI, echo=echo)
    yield engine


def retrieve_root() -> pl.DataFrame:
    with initialize_engine() as conn:
        query = "SELECT * FROM root"
        df = pl.read_database(query=query, connection=conn.connect())
        return df


def retrieve_dictionary() -> pl.DataFrame:
    with initialize_engine() as conn:
        query = "SELECT * FROM dictionary"
        df = pl.read_database(query=query, connection=conn.connect())
        return df


def search_by_ent_seq(value: int) -> pl.DataFrame:
    dictionary = retrieve_dictionary()
    result = dictionary.select("*").filter(pl.col("ent_seq") == value)
    return result
