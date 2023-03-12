from typing import List, Any, Tuple
import re
from JackAnalyzer.Token import Token

# NOTE: Yes, this is ugly.
#       No, I don't care.
RULES: List[Tuple] = [
    ("//.*", "COMMENT"),
    ("/\*.+\*/", "STAR_COMMENT"),
    ("\\n|\\r", "NEWLINE"),
    (" ", "WHITESPACE"),
    ("[a-zA-Z_]\w*", "IDENTIFIER"),
    ("\d+", "INTEGER_CONSTANT"),
    (r"\".*\"", "STRING_CONSTANT"),
    ("[\{\}\(\)\[\]\.\,\;\+\-\*\&\|\<\>\=\~]", "SYMBOL"),
    ("(?<![/\*\d\w])/(?![/\*\d\w])", "TRUE_DIV"),
]

class LexerError(Exception):
    def __init__(self, line_no, column_no, pos):
        self.line_no = line_no
        self.column_no = column_no
        self.pos = pos

class TokenBuilder():
    def __init__(self, block_of_text: str, rules: List[Tuple], keyword_list: list):
        self._buf: str = block_of_text
        self._pos: int = 0
        self._line_start: int = 0
        self._line_no: int = 1
        self._column: int = 0
        self._keyword_list: list = keyword_list
        self.group_map: dict = {}

        parts: List[str] = []

        for idx, element in enumerate(rules):
            name: str = f"GROUP{idx}"
            regexp_group: str = f"(?P<{name}>{element[0]})"
            parts.append(regexp_group)
            self.group_map[name] = element[1]

        self.full_re: str = "|".join(parts)
        self.re_obj: re.Pattern = re.compile(self.full_re)
        self.no_whitespace: re.Pattern = re.compile("\S")

    def __iter__(self):
        return self

    def __next__(self):
        if self._pos >= len(self._buf):
            raise StopIteration()
        else:
            matchobj: re.Match = self.re_obj.match(self._buf, self._pos)
            if matchobj:
                group: str = matchobj.lastgroup
                token_type: str = self.group_map[group]
                self._column = matchobj.start() - self._line_start

                if token_type in ["WHITESPACE"]:
                    self._pos = matchobj.end()
                    return None

                # NOTE: There's a conflict between the regex that matches identifiers and
                #       the one that matches keywords. This is how I've decided to resolve
                #       it for now.
                if token_type in ["IDENTIFIER"]:
                    contents: str = matchobj.group(group)
                    if contents in self._keyword_list:
                        token_type = "KEYWORD"

                if token_type in ["NEWLINE"]:
                    self._line_start = matchobj.end()
                    self._pos = matchobj.end()
                    self._line_no += 1
                    return None

                if token_type in ["COMMENT", "STAR_COMMENT"]:
                    self._pos = matchobj.end()
                    return None

                # token: tuple = (token_type, matchobj.group(group), self._pos, self._line_no, self._column)
                token: Token = Token(token_type, matchobj.group(group), self._line_no, self._column, self._pos)
                self._pos = matchobj.end()
                return token

            raise LexerError(self._pos, self._buf[self._pos])
