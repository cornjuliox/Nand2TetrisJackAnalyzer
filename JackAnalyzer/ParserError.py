from typing import Union
from JackAnalyzer.Token import Token, List

class ParserError(Exception):
    def __init__(self, token: Union[Token, None], message: str, stream: List):
        self.token: Union[Token, None] = token
        self.message: str = message
        self.stream: List = stream
