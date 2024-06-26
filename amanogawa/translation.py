from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from requests import Response

import devtools as dev
import requests

from amanogawa.config import G_API_KEY
from amanogawa.config import G_PROJECT_ID


HEADERS = {
    "Authorization": f"Bearer {G_API_KEY}",
    "x-goog-user-project": G_PROJECT_ID,
    "Content-Type": "application/json; charset=utf-8"
}

def get_language_id() -> Response:
    response = requests.get(
        url="https://translation.googleapis.com/language/translate/v2/languages",
        headers=HEADERS,
    )
    return response


def translate(text: str) -> Response:
    response = requests.post(
        url="https://translation.googleapis.com/language/translate/v2",
        headers=HEADERS,
        json={
            "q": text,
            "source": "ja",
            "target": "en",
            "format": "text",
        },
    )

    return response


if __name__ == '__main__':
    response = translate("-た")

    if response.status_code == 200:
        dev.debug(response.json())
    else:
        dev.debug(vars(response))
