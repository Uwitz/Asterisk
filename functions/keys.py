from typing import Optional

from functions.objects import RequestSignature

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
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

	def sign(self, data: str) -> RequestSignature:
		timestamp: str = datetime.now().isoformat()
		private_key = ec.derive_private_key(
			int.from_bytes(self.private_key, 'big'),
			ec.SECP521R1(),
			default_backend()
		)
		signer = private_key.signer(ec.ECDSA(hashes.SHA256()))
class ECDSA:
	def __init__(self, signing_key: Optional[SigningKey]):
		self.signing_key = signing_key

	def generate_keypair(self, store: Optional[bool] = False):
		self.signing_key = SigningKey.generate(curve = SECP256k1)
		open("./resources/signing_key.pem", "wb").write(self.signing_key.to_pem()) if store else None
		return self.signing_key.verifying_key


		return RequestSignature(
			headers = {
				"X-Signature-Timestamp": timestamp,
				"X-Signature-Ed25519": signer.update(f'{timestamp}{data}'.encode()).finalize()
			},
			data = data
		)

	@staticmethod
	async def verify(public_key: bytes, data: str, signature: str, timestamp: str) -> bool:
		try:
			VerifyKey(public_key).verify(f'{timestamp}{data}'.encode(), bytes.fromhex(signature))
			return True
		except BadSignatureError:
			return False