from typing import List

from Token import Token
from ParserError import ParserError

class ParserBase():
    def __init__(self, tokens: List[Token]):
        self._tokens: List[Token] = tokens

    def peek(self):
        return self._tokens[0]

    def lookahead(self, offset=1):
        return self._tokens(offset)

    def scan_token(self):
        return self._tokens.pop(0)

    def expect_token(self, token_type: str, val: str = None, mult: List[str] = None):
        next_token_type = self.top.type
        expected_token_type = token_type
        err_type: str = f"Expected type {token_type}, but got {next_token_type} instead!"

        if val:
            next_token_val = self.top.value
            expected_token_val = val
            try:
                assert expected_token_val == next_token_val
            except AssertionError:
                err_val: str = f"Expected value {expected_token_val}, but got {next_token_val} instead!"
                raise ParserError(self.top, err_val)

        if mult:
            next_token_val = self.top.value
            err_mult = f"Expected value to be one of {mult}, but got {next_token_val} instead!"
            if next_token_val in mult:
                return self.scan_token()
            else:
                raise ParserError(self.top, err_mult)

        if next_token_type == expected_token_type:
            return self.scan_token()
        else:
            raise ParserError(self.top, err_type)
