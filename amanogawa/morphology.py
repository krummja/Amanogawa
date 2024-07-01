from __future__ import annotations
from typing import *


class MorphemeInfo(NamedTuple):
    dictionary_form: str
    surface_form: str
    reading_form: str
    category_0: str
    category_1: str
    category_2: str
    category_3: str
    conjugation_type: str  # informs e.g. the onbin stem form
    conjugation_form: str

    def __str__(self) -> str:
        return (f"<{self.dictionary_form}> :: " or "") + " | ".join([
            self.category_0 or "*",
            self.category_1 or "*",
            self.category_2 or "*",
            self.category_3 or "*",
            self.conjugation_type or "*",
            self.conjugation_form or "*",
        ])
