from typing import Any, List
from xml.etree.ElementTree import Element

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
