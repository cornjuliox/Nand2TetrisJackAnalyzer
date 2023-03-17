from JackAnalyzer.Token import Token, List

class ParserError(Exception):
    def __init__(self, token: Token, message: str, stream: List):
        self.token: Token = token
        self.message: str = message
        self.stream: List = stream
