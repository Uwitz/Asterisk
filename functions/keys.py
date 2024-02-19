from typing import Optional

from functions.objects import RequestSignature

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

from datetime import datetime

class ECC:
	def __init__(self, private_key: Optional[bytes]):
		self.private_key = private_key

	def generate_keypair() -> bytes:
		private_key = ec.generate_private_key(
			ec.SECP521R1(),
			default_backend()
		)

		private_key_bytes = private_key.private_bytes(
			encoding = serialization.Encoding.PEM,
			format = serialization.PrivateFormat.PKCS8,
			encryption_algorithm = serialization.NoEncryption()
		)

		open("./resources/private_key.pem", "wb").write(private_key_bytes)

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

		return RequestSignature(
			headers = {
				"X-Signature-Timestamp": timestamp,
				"X-Signature-Ed25519": signer.update(f'{timestamp}{data}'.encode()).finalize()
			},
			data = data
		)