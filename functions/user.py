import os
import json

from typing import Optional
from aiohttp import ClientSession
from pathlib import Path

from functions.keys import ECC

class User:
    def __init__(
            self,
            user_credentials: Optional[dict],
            session_token: Optional[str]
        ):
        self.credentials = user_credentials
        self.session_token = session_token

    def fetch_local(self) -> dict | None:
        self.credentials: dict | None = json.load(open("./resources/credentials.json")) if Path("./resources/credentials.json").is_file() else None
        return self.credentials