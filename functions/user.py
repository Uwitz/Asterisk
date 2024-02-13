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

    @staticmethod
    async def create_user(username: str) -> dict:
        public_key = ECC().generate_keypair()
        if Path("./resources/server_conf.json"):
            server_conf: dict = json.load(open("./resources/server_conf.json"))

        else:
            json.dump(
                {
                    1: "1.snys.snyco.uk",
                    2: "2.snys.snyco.uk",
                    3: "3.snys.snyco.uk",
                    4: "4.snys.snyco.uk"
                },
                open("server_conf.json", "w", encoding = "utf-8"),
                ensure_ascii = False,
                indent = 4
            )
            server_conf: dict = {
                1: "1.snys.snyco.uk",
                2: "2.snys.snyco.uk",
                3: "3.snys.snyco.uk",
                4: "4.snys.snyco.uk"
            }

        async with ClientSession() as session:
            async with session.request(
                "POST",
                "https://sync.synco.uk/user/create",
                json = {
                    "username": username,
                    "public_key": public_key,
                    "server_conf": server_conf
                }
            ) as response:
                if response.status in (200, 201):
                    response_json = response.json()
                    return User(
                        {
                            "username": response_json.get("username")
                        },
                        response_json.get("session_token")
                    )