import json

from functions.keys import ECC
from functions.user import User
from functions.objects import SessionToken

from pathlib import Path
from typing import Dict, Optional, Union
from aiohttp import ClientSession

class Session:
    def __init__(self, token: Optional[str], server_conf: Optional[Dict[Union[int, str], str]]):
        self.token = token
        self.server_conf = server_conf or json.load(open("./resources/server_conf.json", "r")) or {
            "auth": "auth.snys.snyco.uk",
            1: "1.snys.snyco.uk",
            2: "2.snys.snyco.uk",
            3: "3.snys.snyco.uk",
            4: "4.snys.snyco.uk"
        }
        json.dump(self.server_conf, open("./resources/server_conf.json", "w")) if self.server_conf != json.load(open("./resources/server_conf.json", "r")) else None

    async def authenticate(self, auth_server: Optional[str]) -> str:
        ...

