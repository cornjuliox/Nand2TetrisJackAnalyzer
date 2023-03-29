from typing import List, Union
from xml.etree.ElementTree import Element
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

    def expect_token(self, token_type: str, val: Union[str, None] = None, mult: Union[List[str], None] = None) -> Element:
        try:
            next_token_type = self.top.tag
        except IndexError:
            raise

        err_type: str = f"Expected type {token_type}, but got {next_token_type} instead!"
        expected_token_type = token_type

        if val:
            next_token_val = self.top.text
            expected_token_val = val
            try:
                assert expected_token_val == next_token_val
            except AssertionError:
                err_val: str = f"Expected value {expected_token_val}, but got {next_token_val} instead!"
                raise ParserError(self.top, err_val, self._tokens)

        if mult:
            next_token_val = self.top.text
            err_mult = f"Expected value to be one of {mult}, but got {next_token_val} instead!"
            if next_token_val in mult:
                return self.scan_token()
            else:
                raise ParserError(self.top, err_mult, self._tokens)

        if next_token_type == expected_token_type:
            return self.scan_token()
        else:
            raise ParserError(self.top, err_type, self._tokens)
        
    def _match_type(self) -> Element:
        """ Matches the 'type' rule. """
        try:
            var_type: Element = self.expect_token("keyword", mult=["int", "char", "boolean"])
        except ParserError:
            var_type = self.expect_token("identifier")

        return var_type

    def _match_identifier(self) -> Element:
        """ Matches either className, subroutineName, varName rules. """
        identifier: Element = self.expect_token("identifier")
        return identifier

    def _match_op(self) -> Element:
        op: Element = self.expect_token("symbol", mult=["+", "-", "*", "/", "&", "|", "<", ">", "="])
        return op

    def _match_unary_op(self) -> Element:
        op: Element = self.expect_token("symbol", mult=["-", "~"])
        return op

    def _match_keyword_constant(self) -> Element:
        kw_constant: Element = self.expect_token("keyword", mult=["true", "false", "null", "this"])
        return kw_constant

    def _match_integer_constant(self) -> Element:
        int_constant: Element = self.expect_token("integerConstant")
        # value should be between 0 - 32767
        if int(int_constant.text) < 0 or int(int_constant.text) > 32767: 
            raise ParserError(int_constant, "Integer range should be between 0..32767", self._tokens)
        return int_constant

    def _match_string_constant(self) -> Element:
        str_constant: Element = self.expect_token("stringConstant")
        return str_constant
