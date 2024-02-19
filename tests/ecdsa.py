import asyncio

from functions.keys import ECDSA

ecdsa = ECDSA(None)
verifying_key = ecdsa.generate_keypair()
print(verifying_key)

Signature = ecdsa.sign(
    {
        "message": "test"
    }
)
response = asyncio.run(
    ecdsa.verify(
        verifying_key = verifying_key,
        data = {
            "message": "test"
        },
        signature = Signature.headers.get("X-Signature-ECDSA")
    )
)
print(response)
