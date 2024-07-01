from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


DB_USER = os.environ.get("DB_USER", "")
DB_HOST = os.environ.get("DB_HOST", "")
DB_PASS = os.environ.get("DB_PASS", "")
DB_DATABASE = os.environ.get("DB_DATABASE", "")

G_API_KEY = os.environ.get("G_API_KEY", "")
G_ACCESS_TOKEN = os.environ.get("G_ACCESS_TOKEN", "")
G_PROJECT_ID = os.environ.get("G_PROJECT_ID", "")
G_SERVICE_KEY = os.environ.get("G_SERVICE_KEY")

OPEN_AI_KEY = os.environ.get("OPEN_AI_KEY", "")


HERE = Path(__file__)
SRCDIR = HERE.parent
ROOTDIR = SRCDIR.parent
