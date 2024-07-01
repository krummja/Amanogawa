from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from requests import Response

import devtools as dev
from pathlib import Path
from google.cloud import translate_v2
import google.auth

from amanogawa.config import ROOTDIR


class TranslationData(TypedDict):
    translatedText: str
    detectedSourceLanguage: str
    input: str


def translate(text: str) -> TranslationData:
    credentials_file = Path(ROOTDIR, ".gcloud.json")
    credentials, _ = google.auth.load_credentials_from_file(credentials_file)

    translate_client = translate_v2.Client(
        credentials=credentials,
    )

    result = translate_client.translate(text, target_language="en")
    return result


if __name__ == '__main__':
    text = "私の名前はジョナサンです"
    response = translate(text)
    dev.debug(response)
