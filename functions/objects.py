class SessionToken(str):
    def __init__(self, token: str):
        self.token = token

    def __str__(self) -> str:
        return self.token