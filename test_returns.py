from typing import List
from xml.etree.ElementTree import indent, dump
from JackAnalyzer.Token import Token, Node

from utils import make_tokenstream, parser_tester

if __name__ == "__main__":
    sample_return_list: List[str] = [
        "return;",
        "return this;",
        "return a + b;"
    ]
    return_token_list: List[List[Token]] = [make_tokenstream(x) for x in sample_return_list]

    for ts in return_token_list:
        print(f"working on expression list -> {ts}")
        res: Node = parser_tester(ts, "statements")
        indent(res)
        dump(res)
        assert res

    print("finished")
