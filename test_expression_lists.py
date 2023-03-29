from typing import List, Iterable, cast
from xml.etree.ElementTree import indent, dump, Element

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

    expression_list_tokenstreams: List[List[Element]] = [make_tokenstream(x) for x in sample_expression_list]

    for ts in expression_list_tokenstreams:
        working_on: str = ''.join([cast(str, x.text) for x in cast(Iterable[Element], ts)])
        print(f"working on: {working_on}")
        res: Element = parser_tester(ts, "expression_list", debug=False)
        indent(res)
        dump(res)
        assert res is not None
        print()

    print("finished")
