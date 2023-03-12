import pytest
from typing import List, Tuple

from JackAnalyzer.Token import Token, KEYWORD_LIST, Node
from JackAnalyzer.Tokenizer import TokenBuilder, RULES
from JackAnalyzer.Parser import JackParser

# NOTE: What do we do when learning how to write programming languages?
#       write languages to debug our programming languages.
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

@pytest.mark.parametrize("teststr, result", [
    ("sampleFunction()", r"identifier symbol%( node%expressionList symbol%)"),
    ("someClass.someMethod()", r"identifier symbol%. identifier symbol%( node%expressionList symbol%)"),
])
def test_subroutine_call(teststr: str, result: str):
    # NOTE: Prep the tokenstream
    z: TokenBuilder = TokenBuilder(teststr, RULES, KEYWORD_LIST)
    tokenstream: List[Token] = [x for x in z if x]
    j: JackParser = JackParser(tokenstream)
    p: Node =  j.subroutine_call()

    test_tokenstream: List[str] = tokenize_test_string(result)
    for pair in test_tokenstream:
        token: Token = p.pop(0)
        res: Tuple = translate_test_token(pair) 
        expected_type = res[0]
        expected_value = res[1]

        # NOTE: holy SHIT this is messy, fix it later.
        if expected_type.lower() == "node":
            received_type: bool = isinstance(token, Node)
            received_value: str = token.type

            assert received_type
            assert token.type == received_value
        else: 
            received_type: str = token.type
            received_value: str = token.value

            assert expected_type == received_type
            if expected_value is not None:
                assert expected_value == received_value

@pytest.mark.parametrize("teststr, result", [
    ("sampleFunction()", r"identifier symbol%( node%expressionList symbol%)"),
    ("someClass.someMethod()", r"identifier symbol%. identifier symbol%( node%expressionList symbol%)"),
])
def test_subroutine_call(teststr: str, result: str):
    # NOTE: Prep the tokenstream
    z: TokenBuilder = TokenBuilder(teststr, RULES, KEYWORD_LIST)
    tokenstream: List[Token] = [x for x in z if x]
    j: JackParser = JackParser(tokenstream)
    p: Node =  j._subroutine_let()

    test_tokenstream: List[str] = tokenize_test_string(result)
    for pair in test_tokenstream:
        token: Token = p.pop(0)
        res: Tuple = translate_test_token(pair) 
        expected_type = res[0]
        expected_value = res[1]

        # NOTE: holy SHIT this is messy, fix it later.
        if expected_type.lower() == "node":
            received_type: bool = isinstance(token, Node)
            received_value: str = token.type

            assert received_type
            assert token.type == received_value
        else: 
            received_type: str = token.type
            received_value: str = token.value

            assert expected_type == received_type
            if expected_value is not None:
                assert expected_value == received_value

# @pytest.mark.parametrize("teststr, result", [
#     ("12345", r"node%term identifier"),
#     ("\"testStringConstant\"", r"node%term stringConstant"),
#     ("true", r"node%term booleanConstant"),
#     ("false", r""),
#     ("this_is_a_var_name"),
# ])
# def test_simple_term(teststr: str, result: str):
#     # NOTE: a "simple term" is just 'term'
#     #       e.g integerConstant, stringConstant, keywordConstant, varName
#     #       e.g unaryOp + term
#     # NOTE: Prep the tokenstream
#     z: TokenBuilder = TokenBuilder(teststr, RULES, KEYWORD_LIST)
#     tokenstream: List[Token] = [x for x in z if x]
#     j: JackParser = JackParser(tokenstream)
#     p: Node =  j.term()

#     test_tokenstream: List[str] = tokenize_test_string(result)
#     for pair in test_tokenstream:
#         token: Token = p.pop(0)
#         res: Tuple = translate_test_token(pair) 
#         expected_type = res[0]
#         expected_value = res[1]

#         # NOTE: holy SHIT this is messy, fix it later.
#         if expected_type.lower() == "node":
#             received_type: bool = isinstance(token, Node)
#             received_value: str = token.type

#             assert received_type
#             assert token.type == received_value
#         else: 
#             received_type: str = token.type
#             received_value: str = token.value

#             assert expected_type == received_type
#             if expected_value is not None:
#                 assert expected_value == received_value
