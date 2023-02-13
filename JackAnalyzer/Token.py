from typing import Any, List

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

class Token:
    def __init__(self, token_type: str, raw_value: Any, line_no: int, column_no: int, idx: int):
        self.type: str = token_type
        self.value: Any = raw_value
        self.line_no = line_no
        self.column_no = column_no
        self.idx = idx

    def __repr__(self):
        return f"<{self.type} - {self.value} @ line {self.line_no}, col {self.column_no}, pos {self.idx}>".encode("unicode_escape").decode("utf-8")

    def xml(self):
        if self.type == "INTEGER_CONSTANT":
            tag: str = "integerConstant"
        elif self.type == "STRING_CONSTANT":
            tag = "stringConstant"
        else:
            tag: str = self.type.lower()

        template: str = f"<{tag}>{self.value}</{tag}>"
        return template

class ParserToken:
    def __init__(self, name: str):
        self.name: str = name

    def open_tag(self):
        return f"<{self.name}>"
    
    def close_tag(self):
        return f"</{self.name}>"

    def __repr__(self):
        return f"<ParserToken: {self.name}>"

class Node:
    def __init__(self, title: str):
        self._title: str = title
        self._members: List[Node] = []

    def xml(self):
        pass

    def insert(self, new: Token):
        self._members.append(new)
