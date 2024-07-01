from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path
from voicevox import Client
import asyncio

from amanogawa.config import ROOTDIR


async def get_tts(text: str, outfile: str) -> None:
    async with Client() as client:
        audio_query = await client.create_audio_query(text, speaker=11)
        with open(Path(ROOTDIR, f"speech/{outfile}.mp3"), "wb") as f:
            f.write(await audio_query.synthesis(speaker=11))


def text_to_speech(text: str, outfile: str) -> None:
    asyncio.run(get_tts(text, outfile))
