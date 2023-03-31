# NOTE: Lets try this again
from typing import Union, List, Callable, Optional
from xml.etree.ElementTree import Element

from ParserBase import ParserBase
from ParserError import ParserError

class JackParser(ParserBase):
    def _match_recursive_varname(self) -> List[Element]:
        """ 
        Helper function to match 'varName (, varName)*' clusters, recursively if needed. 

        Used in the varDec rule, and the classVarDec rule. Semicolon needs to be matched outside
        this rule.

        Results should ideally be unpacked and stored in a container to prevent nesting. 
        """
        results: List[Element] = []
        var_identifier = self._match_identifier()
        results.append(var_identifier)
        try:
            comma: Element = self.expect_token("symbol", ",")
            results.append(comma)
            return results + self._match_recursive_varname()
        except ParserError:
            return results
        
    def _match_recursive_type_varname(self) -> Union[List, List[Element]]:
        """
        Helper function to match 'type varName (, type varName)*' clusters.

        Used in the parameterList rule.
        """
        # quick bailout - parameter lists can be EMPTY!
        next_token: Element = self.top
        if next_token.tag == "SYMBOL" and next_token.text == ")":
            return [] 
        else:
            results: List[Element] = []
            var_type: Element = self._match_type()
            var_identifier: Element = self._match_identifier()
            results.append(var_type)
            results.append(var_identifier)
            try:
                comma: Element = self.expect_token("symbol", ",")
                results.append(comma)
                return results + self._match_recursive_type_varname()
            except ParserError:
                return results


    def subroutine_parameter_list(self) -> Element:
        """ Matches the parameterList rule. """
        result: Element = Element("parameterList")

        # NOTE: remember that a function doesn't always need parameters.
        #       and that rule is enforced OUTSIDE the recursive_type_varname() command.
        try:
            type_varnames: List[Element] = self._match_recursive_type_varname()
        except ParserError:
            return result

        # NOTE: I hope type_varnames and result are flat.
        result.extend(type_varnames)
        return result

    def _subroutine_while(self) -> Element:
        result: Element = Element("whileStatement")
        while_keyword: Element = self.expect_token("keyword", "while")
        result.append(while_keyword)

        open_paren: Element = self.expect_token("symbol", "(")
        result.append(open_paren)

        expression: Element = self.expression()
        result.append(expression)

        close_paren: Element = self.expect_token("symbol", ")")
        result.append(close_paren)

        open_bracket: Element = self.expect_token("symbol", "{")
        result.append(open_bracket)

        statements: Element = self.statements()
        result.append(statements)

        close_bracket: Element = self.expect_token("symbol", "}")
        result.append(close_bracket)

        return result

    def _subroutine_if(self) -> Element:
        # if (expression) { statements } (else { statements })?
        result: Element = Element("ifStatement")
        if_keyword: Element = self.expect_token("keyword", "if")
        result.append(if_keyword)
        open_paren: Element = self.expect_token("symbol", "(")
        result.append(open_paren)
        expression: Element = self.expression()
        result.append(expression)
        close_paren: Element = self.expect_token("symbol", ")")
        result.append(close_paren)
        open_bracket: Element = self.expect_token("symbol", "{")
        result.append(open_bracket)

        # NOTE: 0 or more statements
        while True:
            if self.top.tag == "symbol" and self.top.text == "}":
                break
            statements: Element = self.statements()
            result.append(statements)

        close_bracket: Element = self.expect_token("symbol", "}")
        result.append(close_bracket)

        # NOTE: 0 or 1 'else' construct, with 0 or more statements
        # NOTE: The 'try' block handles the case where there is no 'else'.
        try:
            if self.top.tag == "keyword" and self.top.text == "else":
                else_kw: Element = self.expect_token("keyword", "else")
                result.append(else_kw)
                open_bracket_2: Element = self.expect_token("symbol", "{")
                result.append(open_bracket_2)
                # while self.top.tag != 'symbol' and self.top.text != '}':
                #     statements2: Element = self.statements()
                #     result.append(statements2)
                while True:
                    if self.top.tag == "symbol" and self.top.text == "}":
                        break
                    statements2: Element = self.statements()
                    result.append(statements2)

                close_bracket_2: Element = self.expect_token("symbol", "}")
                result.append(close_bracket_2)
        except IndexError:
            pass

        return result 

    def _subroutine_let(self) -> Element:
        result: Element = Element("letStatement")

        let_kw: Element = self.expect_token("keyword", "let")
        result.append(let_kw)

        var_name: Element = self.expect_token("identifier")
        result.append(var_name)

        if self.top.tag == "symbol" and self.top.text == "[":
            open_square: Element = self.expect_token("symbol", "[")
            result.append(open_square)

            inner_expression: Element = self.expression()
            result.append(inner_expression)

            close_square: Element = self.expect_token("symbol", "]")
            result.append(close_square)

        equals: Element = self.expect_token("symbol", "=")
        result.append(equals)

        expression: Element = self.expression()
        result.append(expression)

        semicolon: Element = self.expect_token("symbol", ";")
        result.append(semicolon)

        return result

    def _subroutine_do(self) -> Element:
        result: Element = Element("doStatement")
        do_kw: Element = self.expect_token("keyword", "do")
        result.append(do_kw)
        sub_call: List[Element] = self.subroutine_call()
        result.extend(sub_call)
        semicolon: Element = self.expect_token("symbol", ";")
        result.append(semicolon)

        return result
    
    def _subroutine_return(self) -> Element:
        result: Element = Element("returnStatement")
        return_kw: Element = self.expect_token("keyword", "return")
        result.append(return_kw)

        if self.top.tag != "symbol" and self.top.text != ";":
            expression: Element = self.expression()
            result.append(expression)
        else:
            semicolon: Element = self.expect_token("symbol", ";")
            result.append(semicolon)

        return result

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
        
    def subroutine_dec(self) -> Element:
        """ Matches the subroutineDec rule. """
        # NOTE: Subroutine body is nested INSIDE this
        result: Element = Element("subroutineDec")
        subroutine_type: Element = self.expect_token("keyword", mult=["constructor", "function", "method"])
        result.append(subroutine_type)

        try:
            subroutine_datatype: Element = self.expect_token("keyword", "void")
        except ParserError:
            subroutine_datatype = self._match_identifier()

        result.append(subroutine_datatype)
        subroutine_name: Element = self._match_identifier()
        result.append(subroutine_name)
        subroutine_parameter_list_open: Element = self.expect_token("symbol", "(")
        result.append(subroutine_parameter_list_open)
        subroutine_parameter_list: Element = self.subroutine_parameter_list()
        result.append(subroutine_parameter_list)
        subroutine_parameter_list_close: Element = self.expect_token("symbol", ")")
        result.append(subroutine_parameter_list_close)
        subroutine_body: Element = self.subroutine_body()
        result.append(subroutine_body)
        return result

    def subroutine_body(self) -> Element:
        result: Element = Element("subroutineBody")
        open_bracket: Element = self.expect_token("symbol", "{")
        result.append(open_bracket)
        while True:
            if self.top.tag == "keyword" and self.top.text == "var":
                vardecs: Union[Element, None] = self.subroutine_body_var_dec()
                if isinstance(vardecs, Element):
                    result.append(vardecs)
            else:
                break
        statements: Element = self.statements()
        result.append(statements)

        close_bracket: Element = self.expect_token("symbol", "}")
        result.append(close_bracket)
        
        return result

    def subroutine_body_var_dec(self) -> Union[Element, None]:
        """ 
        Matches the 'varDec' rule, and should be written in output as <varDec></varDec>. 
        """
        # NOTE: The following needs to be enforced in the subroutineBody() method.
        #       Needs to be called once per 'var'. Such that the following:
        #       ```
        #       var int a, b;
        #       var int b, c;
        #       ```
        result: Element = Element("varDec")
        # NOTE: Remember that vardec 0 or more. 
        # NOTE: <this> needs to be redone
        if self.top.tag == "keyword" and self.top.text == "var":
            var_kw: Element = self.expect_token("keyword", "var")
            var_type: Element = self._match_type()
            var_names: List[Element] = self._match_recursive_varname()
            semicolon: Element = self.expect_token("symbol", ";")

            result.append(var_kw)
            result.append(var_type)
            result.extend(var_names)
            result.append(semicolon)
        else:
            return None

        return result
        
    def statements(self: 'JackParser') -> Element:
        valid_statements: dict = {
            "let": self._subroutine_let,
            "if": self._subroutine_if,
            "while": self._subroutine_while,
            "do": self._subroutine_do,
            "return": self._subroutine_return,
        }
        results: Element = Element("statements")

        try:
            while self.top.tag == "keyword" and self.top.text in ["if", "let", "do", "while", "return"]:
                target: Callable = valid_statements[self.top.text]
                intermediate_result: Element = target()
                results.append(intermediate_result)
        except IndexError:
            pass

        return results        
        
    def expression_list(self) -> Element:
        result: Element = Element("expressionList")

        # NOTE: Handles empty expression lists; i.e next character is ') '
        if self.top.tag == "symbol" and self.top.text == ")":
            return result
        
        while True:
            expr: Element = self.expression()
            result.append(expr)

            # NOTE: If there's no comma after the first expression, then there's only
            #       one expression, and the next token is a ')'
            try:
                comma: Element = self.expect_token("symbol", ",")
                result.append(comma)
            except IndexError:
                break
            except ParserError:
                if self.top.tag == "symbol" and self.top.text == ")":
                    break
                else:
                    raise

        return result

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
            if isinstance(str_constant, str):
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
    
    def klass_var_dec(self) -> Union[Element, None]:
        result: Element = Element("classVarDec")
        if self.top.tag == "keyword" and self.top.text in ["static", "field"]:
            static_field: Element = self.expect_token("keyword", mult=["static", "field"])
            result.append(static_field)

            var_type: Element = self._match_type()
            result.append(var_type)

            var_name: List[Element] = self._match_recursive_varname()
            result.extend(var_name)

            semicolon: Element = self.expect_token("symbol", ";")
            result.append(semicolon)

            return result
        else:
            return None
    
    # NOTE: This is the entrypoint for the class 
    def klass(self) -> Element:
        result: Element = Element("class")

        class_kw: Element = self.expect_token("keyword", "class")
        result.append(class_kw)

        class_name: Element = self.expect_token("identifier")
        result.append(class_name)

        open_bracket: Element = self.expect_token("symbol", "{")
        result.append(open_bracket)

        class_var_decs: Optional[Element] = self.klass_var_dec()
        if class_var_decs is not None:
            result.append(class_var_decs)

        # subroutine dec function isn't "recursive"?
        # i need to do the recursion here.
        while self.top.tag == "keyword" and self.top.text in ["function", "constructor", "method"]:
            subroutine_dec: Element = self.subroutine_dec()
            result.append(subroutine_dec)
        
        close_bracket: Element = self.expect_token("symbol", "}")
        result.append(close_bracket)

        return result
        
