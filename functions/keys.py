from typing import Any, Optional

from functions.objects import RequestSignature

from ecdsa import SECP256k1, SigningKey, VerifyingKey

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

from datetime import datetime

class ECC:
	def __init__(self, private_key: Optional[bytes]):
		self.private_key = private_key

	def generate_keypair(self, store: Optional[bool] = False) -> bytes:
		private_key = ec.generate_private_key(
			ec.SECP521R1(),
			default_backend()
		)
		private_key_bytes = private_key.private_bytes(
			encoding = serialization.Encoding.PEM,
			format = serialization.PrivateFormat.PKCS8,
			encryption_algorithm = serialization.NoEncryption()
		)
		self.private_key = private_key_bytes
		open("./resources/private_key.pem", "wb").write(private_key_bytes) if store else None

		public_key = private_key.public_key()
		public_key_bytes = public_key.public_bytes(
			encoding = serialization.Encoding.PEM,
			format = serialization.PublicFormat.SubjectPublicKeyInfo
		)
		return public_key_bytes

class ECDSA:
	def __init__(self, signing_key: Optional[SigningKey]):
		self.signing_key = signing_key

	def generate_keypair(self, store: Optional[bool] = False):
		self.signing_key = SigningKey.generate(curve = SECP256k1)
		open("./resources/signing_key.pem", "wb").write(self.signing_key.to_pem()) if store else None
		return self.signing_key.verifying_key

	def sign(self, data) -> RequestSignature:
		signature = self.signing_key.sign(bytes(f"{data}", encoding = "utf-8"))

		return RequestSignature(
			headers = {
				"X-Signature-ECDSA": signature
			},
			data = bytes(f"{data}", encoding = "utf-8")
		)

	@staticmethod
	async def verify(verifying_key: bytes, signature: RequestSignature) -> bool:
		try:
			verifying_key.verify(signature.headers.get("X-Signature-ECDSA"), bytes(f"{signature.data}", encoding = "utf-8"))
			return True
		except:
			return False