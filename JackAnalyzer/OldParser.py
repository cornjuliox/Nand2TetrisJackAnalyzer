from typing import List, Callable, Union, Optional

from JackAnalyzer.Token import Token, Node
from JackAnalyzer.ParserBase import ParserBase
from JackAnalyzer.ParserError import ParserError

        
class JackParser(ParserBase):
    """ For all docstrings, refer to the Jack grammar in Chapter 10, Fig 10.5 of Elements of Computing Systems, 2nd Edition. """
    
    ################### <HELPER FUNCTIONS> ################### 
    ################### <HELPER FUNCTIONS> ################### 
    ################### <HELPER FUNCTIONS> ################### 

    def _match_recursive_type_varname(self) -> Union[List, List[Token]]:
        """
        Helper function to match 'type varName (, type varName)*' clusters.

        Used in the parameterList rule.
        """
        # quick bailout - parameter lists can be EMPTY!
        next_token: Token = self.top
        if next_token.tag == "SYMBOL" and next_token.text == ")":
            return [] 
        else:
            results: List[Token] = []
            var_type: Token = self.match_type()
            var_identifier: Token = self.match_identifier()
            results.append(var_type)
            results.append(var_identifier)
            try:
                comma: Token = self.expect_token("SYMBOL", ",")
                results.append(comma)
                return results + self._match_recursive_type_varname()
            except ParserError:
                return results

    def _match_recursive_varname(self) -> List[Token]:
        """ 
        Helper function to match 'varName (, varName)*' clusters, recursively if needed. 

        Used in the varDec rule, and the classVarDec rule. Semicolon needs to be matched outside
        this rule.

        Results should ideally be unpacked and stored in a container to prevent nesting. 
        """
        results: List[Token] = []
        var_identifier = self.match_identifier()
        results.append(var_identifier)
        try:
            comma: Token = self.expect_token("SYMBOL", ",")
            results.append(comma)
            return results + self._match_recursive_varname()
        except ParserError:
            return results

    ################### </HELPER FUNCTIONS> ################### 
    ################### </HELPER FUNCTIONS> ################### 
    ################### </HELPER FUNCTIONS> ################### 

    ################### <MISC> ################### 
    ################### <MISC> ################### 
    ################### <MISC> ###################

    def match_type(self) -> Token:
        """ Matches the 'type' rule. """
        try:
            var_type: Token = self.expect_token("KEYWORD", mult=["int", "char", "boolean"])
        except ParserError:
            var_type = self.expect_token("IDENTIFIER")

        return var_type

    def match_identifier(self) -> Token:
        """ Matches either className, subroutineName, varName rules. """
        identifier: Token = self.expect_token("IDENTIFIER")
        return identifier

    def match_op(self) -> Token:
        op: Token = self.expect_token("SYMBOL", mult=["+", "-", "*", "/", "&", "|", "<", ">", "="])
        return op

    def match_unary_op(self) -> Token:
        op: Token = self.expect_token("SYMBOL", mult=["-", "~"])
        return op

    def match_keyword_constant(self) -> Token:
        kw_constant: Token = self.expect_token("KEYWORD", mult=["true", "false", "null", "this"])
        return kw_constant

    def match_integer_constant(self) -> Token:
        int_constant: Token = self.expect_token("INTEGER_CONSTANT")
        # value should be between 0 - 32767
        if int(int_constant.text) < 0 or int(int_constant.text) > 32767: 
            raise ParserError(int_constant, "Integer range should be between 0..32767", self._tokens)
        return int_constant

    def match_string_constant(self) -> Token:
        str_constant: Token = self.expect_token("STRING_CONSTANT")
        return str_constant

    ################### </MISC> ################### 
    ################### </MISC> ################### 
    ################### </MISC> ################### 

    ################### <SUBROUTINE SHIT> ################### 
    ################### <SUBROUTINE SHIT> ################### 
    ################### <SUBROUTINE SHIT> ################### 

    def _subroutine_let(self) -> Node:
        result: Node = Node("letStatement")

        let_kw: Token = self.expect_token("KEYWORD", "let")
        result.add(let_kw)

        var_name: Token = self.expect_token("IDENTIFIER")
        result.add(var_name)

        if self.top.tag == "SYMBOL" and self.top.text == "[":
            open_square: Token = self.expect_token("SYMBOL", "[")
            result.add(open_square)

            expression: Node = self.expression()
            result.add(expression)

            close_square: Token = self.expect_token("SYMBOL", "]")
            result.add(close_square)

        equals: Token = self.expect_token("SYMBOL", "=")
        result.add(equals)

        expression = self.expression()
        result.add(expression)

        semicolon: Token = self.expect_token("SYMBOL", ";")
        result.add(semicolon)

        return result

    def _subroutine_if(self) -> Node:
        # if (expression) { statements } (else { statements })?
        result: Node = Node("ifStatement")
        if_keyword: Token = self.expect_token("KEYWORD", "if")
        result.add(if_keyword)
        open_paren: Token = self.expect_token("SYMBOL", "(")
        result.add(open_paren)
        expression: Node = self.expression()
        result.add(expression)
        close_paren: Token = self.expect_token("SYMBOL", ")")
        result.add(close_paren)
        open_bracket: Token = self.expect_token("SYMBOL", "{")
        result.add(open_bracket)
        statements: Optional[Node] = self.statements()
        result.add(statements)

        close_bracket: Token = self.expect_token("SYMBOL", "}")
        result.add(close_bracket)

        if self.top.tag == "KEYWORD" and self.top.text == "else":
            else_kw: Token = self.expect_token("KEYWORD", "else")
            result.add(else_kw)
            open_bracket_2: Token = self.expect_token("SYMBOL", "{")
            result.add(open_bracket_2)
            statements2: Optional[Node] = self.statements()
            result.add(statements2)
            close_bracket_2: Token = self.expect_token("SYMBOL", "}")
            result.add(close_bracket_2)

        return result 

    def _subroutine_while(self) -> Node:
        result: Node = Node("whileStatement")
        while_keyword: Token = self.expect_token("KEYWORD", "while")
        result.add(while_keyword)

        open_paren: Token = self.expect_token("SYMBOL", "(")
        result.add(open_paren)

        expression: Node = self.expression()
        result.add(expression)

        close_paren: Token = self.expect_token("SYMBOL", ")")
        result.add(close_paren)

        open_bracket: Token = self.expect_token("SYMBOL", "{")
        result.add(open_bracket)

        statements: Optional[Node] = self.statements()
        result.add(statements)

        close_bracket: Token = self.expect_token("SYMBOL", "}")
        result.add(close_bracket)

        return result

    def _subroutine_do(self) -> Node:
        result: Node = Node("doStatement")
        do_kw: Token = self.expect_token("KEYWORD", "do")
        result.add(do_kw)
        sub_call: List[Union[Token, Node]] = self.subroutine_call()
        result.add(sub_call)
        semicolon: Token = self.expect_token("SYMBOL", ";")
        result.add(semicolon)

        return result

    def _subroutine_return(self) -> Node:
        result: Node = Node("returnStatement")
        return_kw: Token = self.expect_token("KEYWORD", "return")
        result.add(return_kw)

        if self.top.tag != "SYMBOL" and self.top.text != ";":
            expression: Node = self.expression()
            result.add(expression)
        else:
            semicolon: Token = self.expect_token("SYMBOL", ";")
            result.add(semicolon)

        return result

    def subroutine_dec(self) -> Node:
        """ Matches the subroutineDec rule. """
        # NOTE: Subroutine body is nested INSIDE this
        result: Node = Node("subroutineDec")
        subroutine_type: Token = self.expect_token("KEYWORD", mult=["constructor", "function", "method"])
        result.add(subroutine_type)

        try:
            subroutine_datatype: Token = self.expect_token("KEYWORD", "void")
        except ParserError:
            subroutine_datatype = self.match_identifier()

        result.add(subroutine_datatype)
        subroutine_name: Token = self.match_identifier()
        result.add(subroutine_name)
        subroutine_parameter_list_open: Token = self.expect_token("SYMBOL", "(")
        result.add(subroutine_parameter_list_open)
        subroutine_parameter_list: Node = self.subroutine_parameter_list()
        result.add(subroutine_parameter_list)
        subroutine_parameter_list_close: Token = self.expect_token("SYMBOL", ")")
        result.add(subroutine_parameter_list_close)
        subroutine_body: Node = self.subroutine_body()
        result.add(subroutine_body)
        return result

    def subroutine_parameter_list(self) -> Node:
        """ Matches the parameterList rule. """
        result: Node = Node("parameterList")

        # NOTE: remember that a function doesn't always need parameters.
        #       and that rule is enforced OUTSIDE the recursive_type_varname() command.
        try:
            type_varnames: List[Token] = self._match_recursive_type_varname()
        except ParserError:
            return result

        # NOTE: I hope type_varnames and result are flat.
        result.extend(type_varnames)
        return result

    def subroutine_body_var_dec(self) -> Union[Node, None]:
        """ 
        Matches the 'varDec' rule, and should be written in output as <varDec></varDec>. 
        """
        # NOTE: The following needs to be enforced in the subroutineBody() method.
        #       Needs to be called once per 'var'. Such that the following:
        #       ```
        #       var int a, b;
        #       var int b, c;
        #       ```
        result: Node = Node("varDec")
        # NOTE: Remember that vardec 0 or more. 
        # NOTE: <this> needs to be redone
        if self.top.tag == "KEYWORD" and self.top.text == "var":
            var_kw: Token = self.expect_token("KEYWORD", "var")
            var_type: Token = self.match_type()
            var_names: List[Token] = self._match_recursive_varname()
            semicolon: Token = self.expect_token("SYMBOL", ";")

            result.add(var_kw)
            result.add(var_type)
            result.add(var_names)
            result.add(semicolon)
        else:
            return None

        return result

    def statements(self: 'JackParser') -> Node:
        valid_statements: dict = {
            "let": self._subroutine_let,
            "if": self._subroutine_if,
            "while": self._subroutine_while,
            "do": self._subroutine_do,
            "return": self._subroutine_return,
        }
        results: Node = Node("statements")

        try:
            while self.top.tag == "KEYWORD" and self.top.text in ["if", "let", "do", "while", "return"]:
                target: Callable = valid_statements[self.top.text]
                intermediate_result: Node = target()
                results.add(intermediate_result)
        except IndexError:
            pass

        return results

    def subroutine_body(self) -> Node:
        result: Node = Node("subroutineBody")
        open_bracket: Token = self.expect_token("SYMBOL", "{")
        result.add(open_bracket)
        while True:
            if self.top.tag == "KEYWORD" and self.top.text == "var":
                vardecs: Optional[Node] = self.subroutine_body_var_dec()
                result.add(vardecs)
            else:
                break
        statements: Union[Node, None] = self.statements()
        result.add(statements)

        close_bracket: Token = self.expect_token("SYMBOL", "}")
        result.add(close_bracket)
        
        return result
    
    def subroutine_call(self) -> List[Union[Token, Node]]:
        # there's two forms for this; either a simple `name(expressionList)`
        # call, or a (className|varName)'.'subroutineName(expressionList) version
        
        # className, subroutineName, varName all drill down to "identifier"
        results: List[Union[Token, Node]] = []

        subroutine_or_class_name: Token = self.match_identifier()
        results.append(subroutine_or_class_name)

        if self.top.tag == "SYMBOL":
            if self.top.text == ".":
                dot: Token = self.expect_token("SYMBOL", ".")
                results.append(dot)
                subroutine_name: Token = self.match_identifier()
                results.append(subroutine_name)
                open_paren: Token = self.expect_token("SYMBOL", "(")
                results.append(open_paren)
                expression_list: Node = self.expression_list()
                results.append(expression_list)
                close_paren: Token = self.expect_token("SYMBOL", ")")
                return results

        open_paren = self.expect_token("SYMBOL", "(")
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
        close_paren = self.expect_token("SYMBOL", ")")
        results.append(close_paren)
        return results

    ################### </SUBROUTINE SHIT> ################### 
    ################### </SUBROUTINE SHIT> ################### 
    ################### </SUBROUTINE SHIT> ################### 

    ################### <EXPRESSIONS> ################### 
    ################### <EXPRESSIONS> ################### 
    ################### <EXPRESSIONS> ################### 
    def _moar_expressions(self) -> List[Union[Token, Node]]:
        # NOTE: I'm not sure that committing to the try-except
        #       style of recursion is beneficial long-term
        try:
            if self.top.tag == "SYMBOL" and self.top.text == ")":
                return [] 
            else:
                results: List[Union[Node, Token]] = []
                expression: Node = self.expression()
                results.append(expression)
                try:
                    comma: Token = self.expect_token("SYMBOL", ",")
                    results.append(comma)
                    return results + self._moar_expressions()
                except ParserError:
                    return results
        except IndexError:
            return []

    def expression_list(self) -> Node:
        result: Node = Node("expressionList")

        try:
            expressions: List[Union[Token, Node]] = self._moar_expressions()
            result.add(expressions)
        except ParserError:
            result.text = " "
            return result

        return result

    def expression(self) -> Node:
        result: Node = Node("expression")
        term: Node = self.term()
        result.add(term)
        more_terms: bool = True
        while more_terms:
            if self.top.tag == "SYMBOL" and self.top.text in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
                op: Token = self.match_op()
                result.add(op)
                new_term: Node = self.term()
                result.add(new_term)
            else:
                more_terms = False

        return result

    def term(self) -> Node:
        def __handle_int_constant(self: JackParser):
            int_constant: Token = self.match_integer_constant()
            return int_constant 
        
        def __handle_str_constant(self: JackParser):
            str_constant: Token = self.match_string_constant()
            return str_constant
        
        def __handle_keyword(self: JackParser):
            kw_constant: Token = self.match_keyword_constant()
            return kw_constant
        
        def __handle_identifier(self: JackParser):
            results: List = []
            varname: Token = self.match_identifier()
            results.append(varname)
            if self.top.tag == "SYMBOL" and self.top.text == "[":
                open_square: Token = self.expect_token("SYMBOL", "[")
                results.append(open_square)
                expression: Node = self.expression()
                results.append(expression)
                close_square: Token = self.expect_token("SYMBOL", "]")
                results.append(close_square)
            elif self.top.tag == "SYMBOL" and self.top.text == ".":
                dot: Token = self.expect_token("SYMBOL", ".")
                results.append(dot)
                subcall: List[Union[Token, Node]] = self.subroutine_call()
                results += subcall

            return results
        
        def __handle_symbol(self: JackParser):
            # remember, "term op term"!
            results: List = []
            if self.top.text == "(":
                open_paren: Token = self.expect_token("SYMBOL", "(")
                results.append(open_paren)
                expressions: Node = self.expression()
                results.append(expressions)
                close_paren: Token = self.expect_token("SYMBOL", ")")
                results.append(close_paren)
                return results
            elif self.top.text in ["~", "-"]: 
                unary_op: Token = self.match_unary_op()
                results.append(unary_op)
                term: Node = self.term()
                results.append(term)
                return results
            else:
                op: Token = self.match_op()
                results.append(op)
                term = self.term()
                results.append(term)
                return results

        result: Node = Node("term")
        current_token_type: str = self.top.tag

        dispatch_table = {
            "INTEGER_CONSTANT": __handle_int_constant,
            "STRING_CONSTANT": __handle_str_constant,
            "KEYWORD": __handle_keyword,
            "IDENTIFIER": __handle_identifier,
            "SYMBOL": __handle_symbol,
        }
        try:
            handler: Callable = dispatch_table[current_token_type]
        except KeyError:
            # treat as a subroutine call
            subcall: List[Union[Token, Node]] = self.subroutine_call()
            result.add(subcall)
            return result

        token_node: Union[Token, Node, List] = handler(self)
        result.add(token_node)

        return result
    

    ################### </EXPRESSIONS> ################### 
    ################### </EXPRESSIONS> ################### 
    ################### </EXPRESSIONS> ################### 
    
    ################### <CLASS LEVEL SHIT> ################### 
    ################### <CLASS LEVEL SHIT> ################### 
    ################### <CLASS LEVEL SHIT> ################### 

    def parse(self):
        return self.klass()

    # NOTE: This is the entrypoint for the class 
    def klass(self) -> Node:
        result: Node = Node("class")

        class_kw: Token = self.expect_token("KEYWORD", "class")
        result.add(class_kw)

        class_name: Token = self.expect_token("IDENTIFIER")
        result.add(class_name)

        open_bracket: Token = self.expect_token("SYMBOL", "{")
        result.add(open_bracket)

        class_var_decs: Node = self.klass_var_dec()
        result.add(class_var_decs)

        # subroutine dec function isn't "recursive"?
        # i need to do the recursion here.
        while self.top.tag == "KEYWORD" and self.top.text in ["function", "constructor", "method"]:
            subroutine_dec: Node = self.subroutine_dec()
            result.add(subroutine_dec)
        
        close_bracket: Token = self.expect_token("SYMBOL", "}")
        result.add(close_bracket)
        
        return result

    def klass_var_dec(self) -> Node:
        result: Node = Node("classVarDec")
        static_field: Token = self.expect_token("KEYWORD", mult=["static", "field"])
        result.add(static_field)

        var_type: Token = self.match_type()
        result.add(var_type)

        var_name: List[Token] = self._match_recursive_varname()
        result.add(var_name)

        semicolon: Token = self.expect_token("SYMBOL", ";")
        result.add(semicolon)

        return result

    ################### </CLASS LEVEL SHIT> ################### 
    ################### </CLASS LEVEL SHIT> ################### 
    ################### </CLASS LEVEL SHIT> ################### 
