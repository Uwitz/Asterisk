from typing import Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

class ECC:
	def __init__(self, private_key: Optional[bytes]):
		self.private_key = private_key

	def generate_keypair() -> bytes:
		private_key = ec.generate_private_key(
			ec.SECP521R1(),  # Specify the curve for maximum security
			default_backend()
		)

		private_key_bytes = private_key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.NoEncryption()
		)

		open("./resources/private_key.pem", "wb").write(private_key_bytes)

		public_key = private_key.public_key()

		public_key_bytes = public_key.public_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PublicFormat.SubjectPublicKeyInfo
		)

		return public_key_bytes