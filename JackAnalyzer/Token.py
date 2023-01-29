from enum import Enum, auto
from typing import Any, List

class TokenType(Enum):
    KEYWORD = auto()
    SYMBOL = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    STRING = auto()

class Token:
    def __init__(self, token_type: str, raw_value: Any, line_no: int, column_no: int, idx: int):
        self.type: str = token_type
        self.raw_value: Any = raw_value
        self.line_no = line_no
        self.column_no = column_no
        self.idx = idx

    def __repr__(self):
        return f"<{self.type} - {self.raw_value} @ line {self.line_no}, col {self.column_no}, pos {self.idx}>".encode("unicode_escape").decode("utf-8")

KEYWORD_LIST: List[str] = [
    "class", "constructor", "function",
    "method", "field", "static",
    "var", "int", "char",
    "boolean", "void", "true",
    "false", "null", "this",
    "let", "do", "if",
    "else", "while", "return",
]

SYMBOL_LIST: List[str] = [
    "{", "}", "(", ")", "[", "]",
    ".", ",", ";", "+", "-", "*",
    "/", "&", "|", "<", ">", "=",
    "~",
]
