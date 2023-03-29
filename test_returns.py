from typing import List, Iterable, cast
from xml.etree.ElementTree import Element, indent

from utils import make_tokenstream, parser_tester, dump

if __name__ == "__main__":
    sample_return_list: List[str] = [
        "return;",
        "return this;",
        "return a + b;",
        "return some_function();",
        "return someClass.someMethod();"
    ]
    return_token_list: List[List[Element]] = [make_tokenstream(x) for x in sample_return_list]

    for ts in return_token_list:
        working_on: str = ''.join([cast(str, x.text) for x in cast(Iterable[Element], ts)])
        print(f"working on: {working_on}")
        res: Element = parser_tester(ts, "_subroutine_return")
        indent(res)
        dump(res)
        assert res
        print()

    print("finished")
