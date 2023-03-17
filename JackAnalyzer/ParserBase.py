from typing import List

from JackAnalyzer.Token import Token
from JackAnalyzer.ParserError import ParserError

class ParserBase():
    def __init__(self, tokens: List[Token]):
        self._tokens: List[Token] = tokens

    @property
    def top(self):
        return self._tokens[0]

    def peek(self):
        return self._tokens[0]

    def lookahead(self, offset=1):
        return self._tokens[offset]

    def scan_token(self):
        return self._tokens.pop(0)

    def expect_token(self, token_type: str, val: str = None, mult: List[str] = None):

        print(f"current token stream -> {self._tokens}")
        try:
            next_token_type = self.top.type
        except IndexError:
            raise ParserError(None, f"Expected type {token_type} - '{val}', but there are no tokens left to parse!", self._tokens)

        err_type: str = f"Expected type {token_type}, but got {next_token_type} instead!"
        expected_token_type = token_type

        if val:
            next_token_val = self.top.value
            expected_token_val = val
            try:
                assert expected_token_val == next_token_val
            except AssertionError:
                err_val: str = f"Expected value {expected_token_val}, but got {next_token_val} instead!"
                raise ParserError(self.top, err_val, self._tokens)

        if mult:
            next_token_val = self.top.value
            err_mult = f"Expected value to be one of {mult}, but got {next_token_val} instead!"
            if next_token_val in mult:
                return self.scan_token()
            else:
                raise ParserError(self.top, err_mult, self._tokens)

        if next_token_type == expected_token_type:
            return self.scan_token()
        else:
            raise ParserError(self.top, err_type, self._tokens)
