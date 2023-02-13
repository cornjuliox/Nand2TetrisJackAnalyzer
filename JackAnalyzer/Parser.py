from typing import List, Union, Callable

from Token import Token
from ParserBase import ParserBase
from ParserError import ParserError

class ParserContainer():
    def __init__(self, name: str):
        self._children = []
        self.name = name

    def __iter__(self):
        return self

    def __next__(self):
        next_item = self._children.pop(0)
        try:
            yield next_item
        except IndexError:
            raise StopIteration

    # Don't call this yet!
    def form(self):
        template: str = []
        template.append(f"<{self.name}>")
        for x in self._children:
            data: str = x.xml()
            template.append(data)
        template.append(f"</{self.name}>")
        return template

    # I could probably override '+' for this
    # but I don't want to go that far.
    # Containers are gonna need to nest but I don't know
    # how to handle that just yet....
    def add(self, thing):
        self._children.append(thing)
        
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
        results: List[Token] = []
        var_type: Token = self.match_type()
        var_identifier: Token = self.match_identifier()
        results.append(var_type)
        results.append(var_identifier)
        try:
            comma: Token = self.expect_token("SYMBOL", ",")
            results.append(comma)
            return results + self.match_type_varname()
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

    def _subroutine_let(self) -> ParserContainer:
        result: ParserContainer = ParserContainer("letStatement")
        pass

    def _subroutine_if(self) -> ParserContainer:
        result: ParserContainer = ParserContainer("ifStatement")
        pass

    def _subroutine_while(self) -> ParserContainer:
        result: ParserContainer = ParserContainer("whileStatement")
        pass

    def _subroutine_do(self) -> ParserContainer:
        result: ParserContainer = ParserContainer("doStatement")
        pass

    def _subroutine_return(self) -> ParserContainer:
        result: ParserContainer = ParserContainer("returnStatement")
        pass

    def subroutine_dec(self) -> ParserContainer:
        """ Matches the subroutineDec rule. """
        # NOTE: Subroutine body is nested INSIDE this
        result: ParserContainer = ParserContainer("subroutineDec")
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
        subroutine_parameter_list: ParserContainer = self.subroutine_parameter_list(self)
        result.add(subroutine_parameter_list)
        subroutine_parameter_list_close: Token = self.expect_token("SYMBOL", ")")
        result.add(subroutine_parameter_list_close)
        subroutine_body: ParserContainer = self.subroutine_body()
        result.add(subroutine_body)
        return result

    def subroutine_parameter_list(self) -> ParserContainer:
        """ Matches the parameterList rule. """
        result: ParserContainer = ParserContainer("parameterList")

        # NOTE: remember that a function doesn't always need parameters.
        #       and that rule is enforced OUTSIDE the recursive_type_varname() command.
        try:
            type_varnames: List[Token] = self._match_recursive_type_varname()
        except ParserError:
            return result

        # NOTE: I hope type_varnames and result are flat.
        result.add(type_varnames)
        return result

    def subroutine_body_var_dec(self) -> ParserContainer:
        """ 
        Matches the 'varDec' rule, and should be written in output as <varDec></varDec>. 

        would generate x2 ParserContainer instances.
        """
        # NOTE: The following needs to be enforced in the subroutineBody() method.
        #       Needs to be called once per 'var'. Such that the following:
        #       ```
        #       var int a, b;
        #       var int b, c;
        #       ```
        result: ParserContainer = ParserContainer("classVarDec")
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
        results: ParserContainer = ParserContainer("statements")
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
            intermediate_result: ParserContainer = target()
            results.add(intermediate_result)
            # NOTE: Check this later...
            return results + self.subroutine_body_statements()
        else:
            return results


    def subroutine_body(self) -> ParserContainer:
        result: ParserContainer = ParserContainer("subroutineBody")
        open_bracket: Token = self.expect_token("SYMBOL", "{")
        result.add(open_bracket)

        statements: List[ParserContainer] = self.subroutine_body_statements()
        result.add(statements)
        
        return result

    ################### </SUBROUTINE SHIT> ################### 
    ################### </SUBROUTINE SHIT> ################### 
    ################### </SUBROUTINE SHIT> ################### 

    ################### <EXPRESSIONS> ################### 
    ################### <EXPRESSIONS> ################### 
    ################### <EXPRESSIONS> ################### 

    # wow this one is hard

    ################### </EXPRESSIONS> ################### 
    ################### </EXPRESSIONS> ################### 
    ################### </EXPRESSIONS> ################### 
    
    # NOTE: This is the entrypoint for the class
    def klass(self):
        pass
