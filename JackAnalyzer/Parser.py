from typing import List, Callable, Union

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
        if next_token.type == "SYMBOL" and next_token.value == ")":
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
        if int(int_constant.value) < 0 or int(int_constant.value) > 32767: 
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

        if self.top.type == "SYMBOL" and self.top.value == "[":
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
        result: Node = Node("ifStatement")
        return result 

    def _subroutine_while(self) -> Node:
        result: Node = Node("whileStatement")
        return result

    def _subroutine_do(self) -> Node:
        result: Node = Node("doStatement")
        do_kw: Token = self.expect_token("KEYWORD", "do")
        result.add(do_kw)
        sub_call: List[Union[Token, Node]] = self.subroutine_call()
        result.add(sub_call)

        return result

    def _subroutine_return(self) -> Node:
        result: Node = Node("returnStatement")
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

    def subroutine_body_statements(self: 'JackParser') -> Union[Node, None]:
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
        current_val: str =  self.top.value

        if current_type == "KEYWORD" and current_val in valid_statements:
            results: Node = Node("statements")
            target: Callable = valid_statements[current_val]
            intermediate_result: Node = target()
            results.add(intermediate_result)
            # NOTE: This seems iffy; revisit later
            # NOTE: Should we recurse and let the subsequent call bail out? 
            return self.subroutine_body_statements()
        else:
            return None 

    def subroutine_body(self) -> Node:
        result: Node = Node("subroutineBody")
        open_bracket: Token = self.expect_token("SYMBOL", "{")
        result.add(open_bracket)
        vardecs: Node = self.subroutine_body_var_dec()
        result.add(vardecs)
        statements: Union[Node, None] = self.subroutine_body_statements()
        result.add(statements)
        
        return result
    
    def subroutine_call(self) -> List[Union[Token, Node]]:
        # there's two forms for this; either a simple `name(expressionList)`
        # call, or a (className|varName)'.'subroutineName(expressionList) version
        
        # className, subroutineName, varName all drill down to "identifier"
        results: List[Union[Token, Node]] = []

        subroutine_or_class_name: Token = self.match_identifier()
        results.append(subroutine_or_class_name)

        if self.top.type == "SYMBOL":
            if self.top.value == ".":
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
        if self.top.type == "SYMBOL" and self.top.value == ")":
            # NOTE: bail immediately if you see the ')' next
            close_paren = self.expect_token("SYMBOL", ")")
            results.append(close_paren)
            return results
        else:
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

    # NOTE: needs to be expressionList -> expression -> term

    def _moar_expressions(self) -> List[Union[Token, Node]]:
        try:
            if self.top.type == "SYMBOL" and self.top.value == ")":
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
        # import pdb
        # pdb.set_trace()
        result: Node = Node("expressionList")
        try:
            expressions: List[Union[Token, Node]] = self._moar_expressions()
            result.add(expressions)
        except ParserError:
            return result

        return result

    def expression(self) -> Node:
        result: Node = Node("expression")
        term: Node = self.term()
        result.add(term)
        more_terms: bool = True
        while more_terms:
            if self.top.type == "SYMBOL" and self.top.value in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
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
            if self.top.type == "SYMBOL" and self.top.value == "[":
                open_square: Token = self.expect_token("SYMBOL", "[")
                results.append(open_square)
                expression: Node = self.expression()
                results.append(expression)
                close_square: Token = self.expect_token("SYMBOL", "]")
                results.append(close_square)
            elif self.top.type == "SYMBOL" and self.top.value == ".":
                dot: Token = self.expect_token("SYMBOL", ".")
                results.append(dot)
                subcall: List[Union[Token, Node]] = self.subroutine_call()
                results += subcall

            return results
        
        def __handle_symbol(self: JackParser):
            # remember, "term op term"!
            results: List = []
            if self.top.value == "(":
                open_paren: Token = self.expect_token("SYMBOL", "(")
                results.append(open_paren)
                expressions: Node = self.expression()
                results.append(expressions)
                close_paren: Token = self.expect_token("SYMBOL", ")")
                results.append(close_paren)
                return results
            elif self.top.value in ["~", "-"]: 
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
        current_token_type: str = self.top.type

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
    
    def _op_term(self):
        pass

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
