import pytest
from typing import List, Tuple

from JackAnalyzer.Token import Token, KEYWORD_LIST, Node
from JackAnalyzer.Tokenizer import TokenBuilder, RULES
from JackAnalyzer.Parser import JackParser

# NOTE: What do we do when learning how to write programming languages?
#       write programming languages to debug our programming languages.
#       Instead of using tuples to specify test criteria, I can write something more concise i.e
#       keyword%static, keyword%int, identifier, symbol%;, symbol%,
#       <type>%<value>
#       separated by spaces because they don't mean anything, and % because it's not
#       used in Jack.

def tokenize_test_string(teststr: str) -> List[str]:
    return teststr.split()

def translate_test_token(token: str):
    parts: List = token.split("%")
    token_type: str = parts[0].upper()
    if token_type == "IDENTIFIER":
        return (token_type, None)
    else:
        token_value: str = parts[1]
        return (token_type, token_value)
    

@pytest.mark.parametrize("teststr, result", [
    ("static int testvar1;", r"keyword%static keyword%int identifier symbol%;"),
    ("static boolean testvar1;", r"keyword%static keyword%boolean identifier symbol%;"),
    ("static char testvar;", r"keyword%static keyword%char identifier symbol%;"),
    ("field int testvar1;", r"keyword%field keyword%int identifier symbol%;"),
    ("field char testvar2;", r"keyword%field keyword%char identifier symbol%;"),
    ("field boolean testvar3;", r"keyword%field keyword%boolean identifier symbol%;"),
    (
        "static int test1, test2, test3, test4, test5;",
        r"keyword%static keyword%int identifier symbol%, identifier symbol%, identifier symbol%, identifier symbol%, identifier symbol%;"
    ),
    (
        "field char test1, test2;",
        r"keyword%field keyword%char identifier symbol%, identifier symbol%;"
    )
    
])
def test_class_var_dec_2(teststr: str, result: str):
    # NOTE: Prep the tokenstream
    z: TokenBuilder = TokenBuilder(teststr, RULES, KEYWORD_LIST)
    tokenstream: List[Token] = [x for x in z if x]
    j: JackParser = JackParser(tokenstream)
    p: Node =  j.klass_var_dec()

    test_tokenstream: List[str] = tokenize_test_string(result)
    for pair in test_tokenstream:
        token: Token = p._children.pop(0)
        print(token)
        res: Tuple = translate_test_token(pair) 
        expected_type = res[0]
        expected_value = res[1]
        
        received_type: str = token.type
        received_value: str = token.value

        assert expected_type == received_type
        if expected_value is not None:
            assert expected_value == received_value

@pytest.mark.parametrize("teststr, result", [
    # ("", None), <- this case might need to be tested further up, because the parenthesis are not a part of this rule
    # they are outside of it and passing an empty string will just cause the parser to complain.
    (")", ""),
    ("int ax, int bx, int cx", r"keyword%int identifier symbol%, keyword%int identifier symbol%, keyword%int identifier"),
    ("int ax, int bx", r"keyword%int identifier symbol%, keyword%int identifier"),
    ("int ax", r"keyword%int identifier"),
])
def test_parameter_list_dec_2(teststr: str, result: str):
    # NOTE: Prep the tokenstream
    z: TokenBuilder = TokenBuilder(teststr, RULES, KEYWORD_LIST)
    tokenstream: List[Token] = [x for x in z if x]
    j: JackParser = JackParser(tokenstream)
    p: Node =  j.subroutine_parameter_list()

    test_tokenstream: List[str] = tokenize_test_string(result)
    for pair in test_tokenstream:
        token: Token = p._children.pop(0)
        res: Tuple = translate_test_token(pair) 
        expected_type = res[0]
        expected_value = res[1]
        
        received_type: str = token.type
        received_value: str = token.value

        assert expected_type == received_type
        if expected_value is not None:
            assert expected_value == received_value

@pytest.mark.skip()
@pytest.mark.parametrize("teststr, result", [
    (
        "int ax, int bx, int cx, int dx",
        [
            ("KEYWORD", "int"),
            ("IDENTIFIER", None),
            ("SYMBOL", ","),
            ("KEYWORD", "int"),
            ("IDENTIFIER", None),
            ("SYMBOL", ","),
            ("KEYWORD", "int"),
            ("IDENTIFIER", None),
            ("SYMBOL", ","),
            ("KEYWORD", "int"),
            ("IDENTIFIER", None),
        ]
    ),
    (
        "char ax, char bx",
        [
            ("KEYWORD", "char"),
            ("IDENTIFIER", None),
            ("SYMBOL", ","),
            ("KEYWORD", "char"),
            ("IDENTIFIER", None),
        ]
    ),
    (
        "boolean ax, boolean bx",
        [
            ("KEYWORD", "boolean"),
            ("IDENTIFIER", None),
            ("SYMBOL", ","),
            ("KEYWORD", "boolean"),
            ("IDENTIFIER", None),
        ]
    ),
    (
        "int ax",
        [
            ("KEYWORD", "int"),
            ("IDENTIFIER", None),
        ]
    ),
    (
        "char ax",
        [
            ("KEYWORD", "char"),
            ("IDENTIFIER", None),
        ]
    ),
    (
        "boolean ax",
        [
            ("KEYWORD", "boolean"),
            ("IDENTIFIER", None),
        ]
    ),
])
def test_paramter_list_dec(teststr: str, result: List):
    """ Tests the parameterList rule from the grammar spec. """
    z: TokenBuilder = TokenBuilder(teststr, RULES, KEYWORD_LIST)
    tokenstream: List[Token] = [x for x in z if x]
    j: JackParser = JackParser(tokenstream)
    p: ParserContainer = j.subroutine_parameter_list()
    for pair in result:
        token = p._children.pop(0)
        expected_type = pair[0]
        expected_value = pair[1]

        received_type = token.type
        received_value = token.value

        assert received_type == expected_type
        if expected_value is not None:
            assert received_value == expected_value

# do moveSquare();
# do Screen.moveSquare();
@pytest.mark.skip()
@pytest.mark.parametrize("teststr, result", [
    ("moveSquare()", [("IDENTIFIER", None), ("SYMBOL", "("), ("PARSERCONTAINER", "expressionList"), ("SYMBOL", ")")]),
    ("Screen.moveSquare()", [])
])
def test_subroutine_call_parser(teststr: str, result: List):
    # NOTE: Should be <symbol>(</symbol<expressionList></expressionList><symbol>)</symbol>
    #       i.e the ExpressionList does not include its containing parenthesis.
    z: TokenBuilder = TokenBuilder(teststr, RULES, KEYWORD_LIST)
    tokenstream: List[Token] = [x for x in z if x]
    j: JackParser = JackParser(tokenstream)
    p: ParserContainer = j.subroutine_call()
    for pair in result:
        token = p._children.pop(0)
        expected_type = pair[0]
        expected_value = pair[1]
        
        if expected_type == "PARSERCONTAINER":
            assert token.name == expected_value
        else:
            received_type = token.type
            received_value = token.value

            assert received_type == expected_type
            if expected_value is not None:
                assert received_value == expected_value

