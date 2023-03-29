from typing import List
from xml.etree.ElementTree import indent, dump

from JackAnalyzer.Token import Token, Node
from utils import make_tokenstream, parser_tester

if __name__ == "__main__":
    sample_expression_list: List[str] = [
        "", # NOTE: Empty expressionlist
        "true",
        "false",
        "sum / length",
        "x, y, x + 1, y + size",
        "x, y, x + size, y + size",
    ]

    expression_list_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_expression_list]

    for ts in expression_list_tokenstreams:
        print(f"working on expression list -> {''.join([x.text for x in ts])}")
        res: Node = parser_tester(ts, "expression_list", debug=False)
        indent(res)
        dump(res)
        assert res is not None
        print()

    print("finished")
