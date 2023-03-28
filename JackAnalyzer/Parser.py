# NOTE: Lets try this again
from typing import Union, List, Callable
from xml.etree.ElementTree import Element

from JackAnalyzer.ParserBase import ParserBase
from JackAnalyzer.ParserError import ParserError

class JackParser(ParserBase):
    def _match_type(self) -> Element:
        """ Matches the 'type' rule. """
        try:
            var_type: Element = self.expect_token("KEYWORD", mult=["int", "char", "boolean"])
        except ParserError:
            var_type = self.expect_token("IDENTIFIER")

        return var_type

    def _match_identifier(self) -> Element:
        """ Matches either className, subroutineName, varName rules. """
        identifier: Element = self.expect_token("IDENTIFIER")
        return identifier

    def _match_op(self) -> Element:
        op: Element = self.expect_token("SYMBOL", mult=["+", "-", "*", "/", "&", "|", "<", ">", "="])
        return op

    def _match_unary_op(self) -> Element:
        op: Element = self.expect_token("SYMBOL", mult=["-", "~"])
        return op

    def _match_keyword_constant(self) -> Element:
        kw_constant: Element = self.expect_token("KEYWORD", mult=["true", "false", "null", "this"])
        return kw_constant

    def _match_integer_constant(self) -> Element:
        int_constant: Element = self.expect_token("INTEGER_CONSTANT")
        # value should be between 0 - 32767
        if int(int_constant.text) < 0 or int(int_constant.text) > 32767: 
            raise ParserError(int_constant, "Integer range should be between 0..32767", self._tokens)
        return int_constant

    def _match_string_constant(self) -> Element:
        str_constant: Element = self.expect_token("STRING_CONSTANT")
        return str_constant

    def term(self) -> Element:
        def __handle_int_constant(self: JackParser):
            int_constant: Element = self._match_integer_constant()
            return int_constant 
        
        def __handle_str_constant(self: JackParser):
            str_constant: Element = self._match_string_constant()
            return str_constant
        
        def __handle_keyword(self: JackParser):
            kw_constant: Element = self._match_keyword_constant()
            return kw_constant
        
        def __handle_identifier(self: JackParser):
            results: List = []
            varname: Element = self._match_identifier()
            results.append(varname)
            if self.top.tag == "SYMBOL" and self.top.text == "[":
                open_square: Element = self.expect_token("SYMBOL", "[")
                results.append(open_square)
                expression: Element = self.expression()
                results.append(expression)
                close_square: Element = self.expect_token("SYMBOL", "]")
                results.append(close_square)
            elif self.top.tag == "SYMBOL" and self.top.text == ".":
                dot: Element = self.expect_token("SYMBOL", ".")
                results.append(dot)
                subcall: List[Union[Element, Element]] = self.subroutine_call()
                results += subcall

            return results
        
        def __handle_symbol(self: JackParser):
            # remember, "term op term"!
            results: List = []
            if self.top.text == "(":
                open_paren: Element = self.expect_token("SYMBOL", "(")
                results.append(open_paren)
                expressions: Element = self.expression()
                results.append(expressions)
                close_paren: Element = self.expect_token("SYMBOL", ")")
                results.append(close_paren)
                return results
            elif self.top.text in ["~", "-"]: 
                unary_op: Element = self._match_unary_op()
                results.append(unary_op)
                term: Element = self._term()
                results.append(term)
                return results
            else:
                op: Element = self._match_op()
                results.append(op)
                term = self.term()
                results.append(term)
                return results

        result: Element = Element("term")
        current_Element_type: str = self.top.tag

        dispatch_table = {
            "INTEGER_CONSTANT": __handle_int_constant,
            "STRING_CONSTANT": __handle_str_constant,
            "KEYWORD": __handle_keyword,
            "IDENTIFIER": __handle_identifier,
            "SYMBOL": __handle_symbol,
        }
        try:
            handler: Callable = dispatch_table[current_Element_type]
        except KeyError:
            # treat as a subroutine call
            subcall: List[Union[Element, Element]] = self.subroutine_call()
            result.add(subcall)
            return result

        Element_Element: Union[Element, Element, List] = handler(self)
        result.add(Element_Element)

        return result
    pass
