from typing import List, cast, Iterable
from xml.etree.ElementTree import indent, Element

from utils import make_tokenstream, parser_tester, dump

terms: List[str] = [
    "i",
    "-j",
    "false",
    "a[1]",
    "a[2]",
    "1",
    "Array.new(length)",
    "\"simple string constant\"",
    "Keyboard.readInt(\"HOW MANY NUMBERS? \")",
    "Screen.drawRectangle(x, y, x + size, y + size)",
]

if __name__ == "__main__":
    term_tokenstreams: List[List[Element]] = [make_tokenstream(x) for x in terms] 

    for ts in term_tokenstreams:
        working_on: str = ''.join([cast(str, x.text) for x in cast(Iterable[Element], ts)])
        print(f"working on: {working_on}")
        res: Element = parser_tester(ts, "term")
        indent(res)
        dump(res)
        assert res
        print()
