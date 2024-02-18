import os
import json

from typing import Optional
from aiohttp import ClientSession
from pathlib import Path

from functions.keys import ECC

class User:
    def __init__(
            self,
            asterisk: str,
            username: str,
            session_token: Optional[str],
            direct_connection: Optional[bool] = False
        ):
        self.asterisk = asterisk
        self.username = username
        self.session_token = session_token
        self.direct_connection = direct_connection

    def fetch_local(self) -> dict | None:
        self.credentials: dict | None = json.load(open("./resources/credentials.json")) if Path("./resources/credentials.json").is_file() else None
        return self.credentials