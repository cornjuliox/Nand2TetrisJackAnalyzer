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

# NOTE: I'm having to differentiate between a 'Token' and a 'Node' in the context of Jack
#       the base elements are keywords, symbols, and identifiers - those become Tokens.
#       'nodes' comprise of 'combinations' of the above 3, and a node contains either nodes
#       or tokens.
# NOTE: I think the way to go is to define __call__() as a standard interface between the two
#       data types, and then standardize on having both return XML of some kind
#       Tokens - return a single xml tag, in a list. i.e <identifier>something</identifier>
#       Nodes - return a list of xml tags, wrapped in a "container" of some kind
#       Why the lists? so I can simplify the outgoing logic, and just += them together to create
#       a single list and then "".join() (or whatever) to produce the final output
class Token(Element):
    def __init__(self, token_type: str, raw_value: Any, line_no: int, column_no: int, idx: int, *args, **kwargs):

        if token_type == "INTEGER_CONSTANT":
            super().__init__("integerConstant", *args, **kwargs)
        elif token_type == "STRING_CONSTANT":
            super().__init__("stringConstant", *args, **kwargs)
        else:
            super().__init__(token_type.lower(), *args, **kwargs)

        self.type: str = token_type
        self.value: Any = raw_value
        self.text: Any = raw_value
        self.line_no: int = line_no
        self.column_no: int = column_no
        self.idx: int = idx

    def __repr__(self):
        # return f"<{self.type} - {self.value} @ line {self.line_no}, col {self.column_no}, pos {self.idx}>".encode("unicode_escape").decode("utf-8")
        return f"< '{self.value}' ({self.type}, {self.line_no} {self.column_no} {self.idx})>".encode("unicode_escape").decode("utf-8")

class Node(Element):
    def __init__(self, nodetype: str):
        super().__init__(nodetype)
        self.type: str = nodetype

    def __repr__(self):
        return f"<Node object of type {self.type}>"

    @property 
    def children(self):
        return self._children
    
    def add(self, thing: Any):
        # maintained for legacy reasons
        try:
            self.append(thing)
        except TypeError:
            pass

        try:
            self.extend(thing)
        except TypeError:
            return
