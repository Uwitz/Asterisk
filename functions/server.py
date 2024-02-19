import json
import uvicorn

from functions.keys import ECC

from aiohttp import ClientSession
from fastapi import FastAPI, HTTPException, Request

app = FastAPI(
	docs_url = None,
	redoc_url = None
)
PUBLIC_KEYS = {}
AUTH_SERVER = json.load(open("./resources/server_conf.json", "r")).get("auth_server")

@app.get("/")
async def hello():
	return "Online"

@app.post("/message")
async def message_event(request: Request):
	if PUBLIC_KEYS.get(request.headers.get("asterisk")) is None:
		async with ClientSession() as session:
			async with session.request("GET", f"https://{AUTH_SERVER}/asterisk/{request.header.get("asterisk")}/public") as response:
				public_key: bytes | None = response.json().get("public_key") if response.status == 200 else None
				PUBLIC_KEYS[request.header.get("asterisk")] = public_key

	else:
		public_key = PUBLIC_KEYS.get(request.headers.get("asterisk"))

	if not ECC.verify(
		public_key = public_key,
		data = request.body.decode("utf-8"),
		signature = request.headers.get("X-Signature-Ed25519"),
		timestamp = request.headers.get("X-Signature-Timestamp")
	): return HTTPException(401, "Invalid Signature")

uvicorn.run(
	"main:app",
	host = '127.0.0.1',
	port = 2201,
	reload = True,
	debug = True,
	workers = 2
)