# NOTE: Lets try this again
from typing import Union, List, Callable
from xml.etree.ElementTree import Element

from JackAnalyzer.ParserBase import ParserBase
from JackAnalyzer.ParserError import ParserError

class JackParser(ParserBase):
    def _moar_expressions(self) -> List[Element]:
        # NOTE: I'm not sure that committing to the try-except
        #       style of recursion is beneficial long-term
        try:
            if self.top.tag == "symbol" and self.top.text == ")":
                return [] 
            else:
                results: List[Element] = []
                expression: Element = self.expression()
                results.append(expression)
                try:
                    comma: Element = self.expect_token("symbol", ",")
                    results.append(comma)
                    return results + self._moar_expressions()
                except ParserError:
                    return results
        except IndexError:
            return []
        
    def expression_list(self) -> Element:
        def __grab_expression(self: JackParser) -> Element:
            expr: Element = self.expression()
            return expr

        result: Element = Element("expressionList")

        # NOTE: Handles empty token stream
        try:
            _ = self.top
        except IndexError:
            return result

        # NOTE: Handles empty expression lists; i.e next character is ') '
        if self.top.tag == "symbol" and self.top.text == ")":
            return result

        while True: 
            expr: Element = __grab_expression(self)
            result.append(expr)

            try:
                _ = self.top
            except IndexError:
                break

            if self.top.tag != "symbol" and self.top.text != ",":
                break

            comma: Element = self.expect_token("symbol", ",")
            result.append(comma)

        return result

    # def expression_list(self) -> Element:
    #     result: Element = Element("expressionList")

    #     try:
    #         expressions: List[Element] = self._moar_expressions()
    #         result.add(expressions)
    #     except ParserError:
    #         result.text = " "
    #         return result

    #     return result

    def subroutine_call(self) -> List[Element]:
        # there's two forms for this; either a simple `name(expressionList)`
        # call, or a (className|varName)'.'subroutineName(expressionList) version
        
        # className, subroutineName, varName all drill down to "identifier"
        results: List[Element] = []

        subroutine_or_class_name: Element = self._match_identifier()
        results.append(subroutine_or_class_name)

        if self.top.tag == "symbol":
            if self.top.text == ".":
                dot: Element = self.expect_token("symbol", ".")
                results.append(dot)
                subroutine_name: Element = self._match_identifier()
                results.append(subroutine_name)
                open_paren: Element = self.expect_token("symbol", "(")
                results.append(open_paren)
                expression_list: Element = self.expression_list()
                results.append(expression_list)
                close_paren: Element = self.expect_token("symbol", ")")
                return results

        open_paren = self.expect_token("symbol", "(")
        results.append(open_paren)
        # NOTE: empty expressions shouldn't appear at all
        # # NOTE: 
        # if self.top.tag == "SYMBOL" and self.top.text == ")":
        #     # NOTE: bail immediately if you see the ')' next
        #     close_paren = self.expect_token("SYMBOL", ")")
        #     results.append(close_paren)
        #     return results
        # else:
        expression_list = self.expression_list()
        results.append(expression_list)
        close_paren = self.expect_token("symbol", ")")
        results.append(close_paren)
        return results

    def expression(self) -> Element:
        result: Element = Element("expression")
        term: Element = self.term()
        result.append(term)

        # NOTE: like with term, an expression can be a single term;
        #       and we need to bail if that's the case.
        try:
            _ = self.top
            more_terms: bool = True
        except IndexError:
            return result

        while more_terms:
            try:
                _ = self.top
            except IndexError:
                break

            if self.top.tag == "symbol" and self.top.text in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
                op: Element = self._match_op()
                result.append(op)
                new_term: Element = self.term()
                result.append(new_term)
            else:
                more_terms = False

        return result

    def term(self) -> Element:
        def __handle_int_constant(self: JackParser):
            int_constant: Element = self._match_integer_constant()
            return int_constant 
        
        def __handle_str_constant(self: JackParser):
            str_constant: Element = self._match_string_constant()
            str_constant.text = str_constant.text.strip("\"")
            return str_constant
        
        def __handle_keyword(self: JackParser):
            kw_constant: Element = self._match_keyword_constant()
            return kw_constant
        
        def __handle_identifier(self: JackParser):
            results: List = []
            varname: Element = self._match_identifier()
            results.append(varname)
            # NOTE: in instances where the term is a single identifier
            #       i.e 'i', this attempt to reference self.top will
            #       raise IndexError as tokenstream is now empty.
            try:
                if self.top.tag == "symbol" and self.top.text == "[":
                    open_square: Element = self.expect_token("symbol", "[")
                    results.append(open_square)
                    expression: Element = self.expression()
                    results.append(expression)
                    close_square: Element = self.expect_token("symbol", "]")
                    results.append(close_square)
                elif self.top.tag == "symbol" and self.top.text == ".":
                    dot: Element = self.expect_token("symbol", ".")
                    results.append(dot)
                    subcall: List[Union[Element, Element]] = self.subroutine_call()
                    results += subcall
            except IndexError:
                pass

            return results
        
        def __handle_symbol(self: JackParser):
            # remember, "term op term"!
            results: List = []
            if self.top.text == "(":
                open_paren: Element = self.expect_token("symbol", "(")
                results.append(open_paren)
                expressions: Element = self.expression()
                results.append(expressions)
                close_paren: Element = self.expect_token("symbol", ")")
                results.append(close_paren)
                return results
            elif self.top.text in ["~", "-"]: 
                unary_op: Element = self._match_unary_op()
                results.append(unary_op)
                term: Element = self.term()
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
            "integerConstant": __handle_int_constant,
            "stringConstant": __handle_str_constant,
            "keyword": __handle_keyword,
            "identifier": __handle_identifier,
            "symbol": __handle_symbol,
        }
        try:
            handler: Callable = dispatch_table[current_Element_type]
        except KeyError:
            # treat as a subroutine call
            subcall: List[Element] = self.subroutine_call()
            result.extend(subcall)
            return result

        Element_Element: Element = handler(self)
        # NOTE: so with Element types, you really have to be careful
        #       about which of the two methods, extend or append, you call
        #       because one will not work right on lists and vice versa 
        try:
            result.append(Element_Element)
        except TypeError:
            result.extend(Element_Element)

        return result
