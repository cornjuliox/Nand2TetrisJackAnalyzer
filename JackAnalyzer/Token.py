from typing import Any, List, Union

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
        # small hack to make the output conform to what the class
        # requries of it.
        if self.type == "INTEGER_CONSTANT":
            tag: str = "integerConstant"
        elif self.type == "STRING_CONSTANT":
            tag = "stringConstant"
        else:
            tag: str = self.type.lower()

        template: str = f"<{tag}>{self.value}</{tag}>"
        return [template]
    
    def __call__(self):
        return self.xml()

class Node:
    def __init__(self, nodetype: str):
        self.type: str = nodetype
        self._children: List[Union[Token, Node]] = []

    def __repr__(self):
        return f"<Node object of type {self.type}>"

    def add(self, thing: Any):
        if isinstance(thing, list):
            for x in thing:
                self._children.append(x)
        else:
            self._children.append(thing)

    def xml(self):
        template: List[str] = []
        open_tag: str = f"<{self.type.lower()}>"
        close_tag: str = f"</{self.type.lower()}>"
        template.append(open_tag)

        for child in self._children:
            template.append(child())

        template.append(close_tag)
        return template
    
    def __call__(self):
        return self.xml()
