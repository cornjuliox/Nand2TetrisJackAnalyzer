from typing import List, Iterable, cast
from xml.etree.ElementTree import Element, indent

from utils import make_tokenstream, parser_tester, dump

if __name__ == "__main__":
    sample_let: list[str] = [
        "let s = \"string constant\";",
        "let z = null;",
        "let a[1] = a[2];",
        "let game = squaregame.new();",
        "let y = y + 2;",
        "let i = i * (-j);",
        "let i = i | j;",
    ]

    let_tokenstreams: List[List[Element]] = [make_tokenstream(x) for x in sample_let] 

    for ts in let_tokenstreams:
        working_on: str = ' '.join([cast(str, x.text) for x in cast(Iterable[Element], ts)])
        print(f"working on: {working_on}")
        res: Element = parser_tester(ts, "_subroutine_let")
        indent(res)
        dump(res)
        assert res
        print()

    print("finished")
