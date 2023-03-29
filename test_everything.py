from typing import List 
from xml.etree.ElementTree import Element

import pytest

from utils import parser_tester, make_tokenstream

@pytest.mark.parametrize("testcases, target_method", [
    ([
        "\"simple string constant\"",
        "Keyboard.readInt(\"HOW MANY NUMBERS? \")",
        "Array.new(length)",
        "i",
        "-j",
        "false",
        "1",
        "a[1]",
        "a[2]" 
    ], "term"),
    ([
        "null",
        "a[2]",
        "i * (-j)",
        "j / (-2)",
        "i | j",
    ], "expression"),
    ([
        "true",
        "false",
        "sum / length",
        "x, y, x + 1, y + size",
        "x, y, x + size, y + size",   
    ], "expression_list"),
])
def test_harness(testcases: List[str], target_method: str) -> None:
    """
    testcases: List[str] -> A list of test cases, i.e terms, expressions, etc.
    target_method: str -> The name of the method used to parse these strings

    returns None.

    raises some flavor of Exception if anything goes wrong.
    """
    tokenstreams: List[List[Element]] = [make_tokenstream(x) for x in testcases]
    for ts in tokenstreams:
        res: Element = parser_tester(ts, target_method)
        assert res is not None
