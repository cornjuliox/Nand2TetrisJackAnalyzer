from typing import List, Callable

from JackAnalyzer.Token import Token, Node
from JackAnalyzer.ParserBase import ParserBase
from JackAnalyzer.ParserError import ParserError

        
class JackParser(ParserBase):
    """ For all docstrings, refer to the Jack grammar in Chapter 10, Fig 10.5 of Elements of Computing Systems, 2nd Edition. """
    
    ################### <HELPER FUNCTIONS> ################### 
    ################### <HELPER FUNCTIONS> ################### 
    ################### <HELPER FUNCTIONS> ################### 

    def _match_recursive_type_varname(self) -> List[Token]:
        """
        Helper function to match 'type varName (, type varName)*' clusters.

        Used in the parameterList rule.
        """
        # quick bailout - parameter lists can be EMPTY!
        next_token: Token = self.top
        if next_token.type == "SYMBOL" and next_token.value == ")":
            return
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
        if int(int_constant.value) < 0 or int(int_constant.value) > 32767: 
            raise ParserError(int_constant, "Integer range should be between 0..32767")
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

        if self.top.type == "SYMBOL" and self.top.value == "[":
            open_square: Token = self.expect_token("SYMBOL", "[")
            result.add(open_square)

            expression: Node = self.expression()
            result.add(expression)

            close_square: Token = self.expect_token("SYMBOL", "]")
            result.add(close_square)

        equals: Token = self.expect_token("SYMBOL", "=")
        result.add(equals)

        expression: Node = self.expression()
        result.add(expression)

        semicolon: Token = self.expect_token("SYMBOL", ";")
        result.add(semicolon)

        return result

    def _subroutine_if(self) -> Node:
        result: Node = Node("ifStatement")
        pass

    def _subroutine_while(self) -> Node:
        result: Node = Node("whileStatement")
        pass

    def _subroutine_do(self) -> Node:
        result: Node = Node("doStatement")
        pass

    def _subroutine_return(self) -> Node:
        result: Node = Node("returnStatement")
        pass

    def subroutine_dec(self) -> Node:
        """ Matches the subroutineDec rule. """
        # NOTE: Subroutine body is nested INSIDE this
        result: Node = Node("subroutineDec")
        subroutine_type: Token = self.expect_token("KEYWORD", mult=["constructor", "function", "method"])
        result.add(subroutine_type)

        try:
            subroutine_datatype: Token = self.expect_token("KEYWORD", "void")
        except ParserError:
            subroutine_datatype: Token = self.match_identifier()

        result.add(subroutine_datatype)
        
        subroutine_name: Token = self.match_identifier()
        result.add(subroutine_name)
        subroutine_parameter_list_open: Token = self.expect_token("SYMBOL", "(")
        result.add(subroutine_parameter_list_open)
        subroutine_parameter_list: Node = self.subroutine_parameter_list(self)
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
        result.add(type_varnames)
        return result

    def subroutine_body_var_dec(self) -> Node:
        """ 
        Matches the 'varDec' rule, and should be written in output as <varDec></varDec>. 

        Each `var` would generate a ParserContainer.
        `var int a, b` -> x1 ParserContainer,
        """
        # NOTE: The following needs to be enforced in the subroutineBody() method.
        #       Needs to be called once per 'var'. Such that the following:
        #       ```
        #       var int a, b;
        #       var int b, c;
        #       ```
        result: Node = Node("classVarDec")
        var_kw: Token = self.expect_token("KEYWORD", "var")
        var_type_identifier: Token = self.match_type()
        var_names: List[Token] = self._match_recursive_varname()
        semicolon: Token = self.expect_token("SYMBOL", ";")
        result.add(var_kw)
        result.add(var_type_identifier)

        for res in var_names:
            result.add(res)

        result.add(semicolon)
        return result

    def subroutine_body_statements(self):
        results: Node = Node("statements")
        valid_statements: dict = {
            "let": self._subroutine_let,
            "if": self._subroutine_if,
            "while": self._subroutine_while,
            "do": self._subroutine_do,
            "return": self._subroutine_return,
        }

        # NOTE: Remember that all calls to self.expect_token()
        #       will either consume the token and move self.top
        #       or raise a ParserError thereby halting the parse.
        current_type: str = self.top.type
        current_val: str =  self.type.value

        if current_type == "KEYWORD" and current_val in valid_statements:
            target: Callable = valid_statements[current_val]
            intermediate_result: Node = target()
            results.add(intermediate_result)
            # NOTE: Check this later...
            return results + self.subroutine_body_statements()
        else:
            return results

    def subroutine_body(self) -> Node:
        result: Node = Node("subroutineBody")
        open_bracket: Token = self.expect_token("SYMBOL", "{")
        result.add(open_bracket)
        vardecs: Node = self.subroutine_body_var_dec()
        result.add(vardecs)
        statements: Node = self.subroutine_body_statements()
        result.add(statements)
        
        return result
    
    def subroutine_call(self) -> List[Token]:
        # there's two forms for this; either a simple `name(expressionList)`
        # call, or a (className|varName)'.'subroutineName(expressionList) version
        
        # className, subroutineName, varName all drill down to "identifier"
        results: List[Token] = []
        subroutine_or_class_name: Token = self.match_identifier()
        results.append(subroutine_or_class_name)

        try:
            open_paren: Token = self.expect_token("SYMBOL", "(")
            results.append(open_paren)
        except ParserError:
            dot: Token = self.expect_token("SYMBOL", ".")
            results.append(dot)
            subroutine_name: Token = self.expect_token("IDENTIFIER")
            results.append(subroutine_name)
            open_paren: Token = self.expect_token("SYMBOL", "(")
            results.append(open_paren)
        
        expression_list: Node = self.expression_list()
        results.append(expression_list)
        close_paren: Token = self.expect_token("SYMBOL", ")")
        results.append(close_paren)
        
        return results

    ################### </SUBROUTINE SHIT> ################### 
    ################### </SUBROUTINE SHIT> ################### 
    ################### </SUBROUTINE SHIT> ################### 

    ################### <EXPRESSIONS> ################### 
    ################### <EXPRESSIONS> ################### 
    ################### <EXPRESSIONS> ################### 

    # NOTE: needs to be expressionList -> expression -> term
    def expression_list(self) -> Node:
        result: Node = Node("expressionList")
        return result

    def expression(self) -> Node:
        result: Node = Node("expression")
        term: Node = self.term()
        result.add(term)
        if self.top.type == "SYMBOL" and self.top.value in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            op_terms: List[Node] = self._op_term()
            result.add(op_terms)
            return result
        else:
            return result

    def term(self) -> Node:
        result: Node = Node("term")

        if self.top.type == "INTEGER_CONSTANT":
            int_constant: Token = self.match_integer_constant()
            result.add(int_constant)
            return result
        elif self.top.type == "STRING_CONSTANT":
            str_constant: Token = self.match_string_constant()
            result.add(str_constant)
            return result
        elif self.top.type == "KEYWORD_CONSTANT":
            kw_constant: Token = self.match_keyword_constant()
            result.add(kw_constant)
            return result
        elif self.top.type == "IDENTIFIER":
            # NOTE: varname has x2 variants here.
            #       varName | varName[expression]
            var_name: Token = self.match_identifier()
            result.add(var_name)
            if self.top.type == "SYMBOL" and self.top.value == "[":
                expression: Node = self.expression()
                result.add(expression)
                close_square: Token = self.expect_token("SYMBOL", "]")
                result.add(close_square)
            if self.top.type == "SYMBOL" and self.top.value == ".":
                dot: Token = self.expect_token("SYMBOL", ".")
                result.add(dot)
                subcall: List[Token] = self.subroutine_call()
                result.add(subcall)
        elif self.top.type == "SYMBOL" and self.top.value == "(":
            expressions_list: Node = self.expression_list()
            result.add(expressions_list)
            close_paren: Token = self.expect_token("SYMBOL", ")")
            result.add(close_paren)
        elif self.top.type == "SYMBOL" and self.top.value in ["~", "-"]:
            unary_op: Token = self.match_unary_op()
            result.add(unary_op)
            term: Node = self.term()
            result.add(term)
        # NOTE: if none of the above pass, then this is a subroutine call.
        else:
            subcall: List[Token] = self.subroutine_call()
            result.add(subcall)

        return result

    def _op_term(self):
        result: List[Token] = []
        op: Token = self._match_op()
        result.add(op)
        try:
            term: Node = self.term()
            result.add(term)
            return result
        except ParserError:
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
    def klass(self):
        result: Node = Node("class")

        class_kw: Token = self.expect_token("KEYWORD", "class")
        result.add(class_kw)

        open_bracket: Token = self.expect_token("SYMBOL", "{")
        result.add(open_bracket)

    def klass_var_dec(self):
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
