class RequestSignature:
    def __init__(self, headers: dict, data: str):
        self.headers = headers
        self.data = data