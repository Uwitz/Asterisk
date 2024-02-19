import json

from functions.keys import ECC
from functions.user import User

from pathlib import Path
from typing import Dict, Optional, Union
from aiohttp import ClientSession

class Session:
	def __init__(self, server_conf: Optional[Dict[Union[int, str], str]]):
		self.server_conf = server_conf or json.load(open("./resources/server_conf.json", "r")) or {
			"auth_server": "auth.snys.snyco.uk",
			1: "1.snys.snyco.uk",
			2: "2.snys.snyco.uk",
			3: "3.snys.snyco.uk",
			4: "4.snys.snyco.uk"
		}
		json.dump(self.server_conf, open("./resources/server_conf.json", "w")) if self.server_conf != json.load(open("./resources/server_conf.json", "r")) else None

	async def authenticate(self, auth_server: Optional[str]) -> str:
		...

	async def create_user(self, asterisk: str, username: str, auth_server: Optional[str], direct_connection: Optional[bool] = False) -> str:
		public_key = ECC().generate_keypair()

		json.dump(self.server_conf, "./resources/server_conf.json") if Path("./resources/server_conf.json") else None

		async with ClientSession() as session:
			async with session.request(
				method = "POST",
				url = auth_server,
				json = {
					"username": username,
					"public_key": public_key,
					"server_conf": self.server_conf
				}
			) as response:
				if response.status in (200, 201):
					response_json = response.json()
					self.user = User(
						username = username,
						asterisk = asterisk,
						session_token = response_json.get("session_token"),
						direct_connection = direct_connection
					)
					return response_json.get("session_token")