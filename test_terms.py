from typing import List
from JackAnalyzer.Token import Token, Node
from xml.etree.ElementTree import indent

from utils import make_tokenstream, parser_tester, dump

terms: List[str] = [
    "\"simple string constant\"",
    "Keyboard.readInt(\"HOW MANY NUMBERS? \")",
    "Array.new(length)",
    "i",
    "-j",
    "false",
    "1",
    "a[1]",
    "a[2]"
]

if __name__ == "__main__":
    term_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in terms] 

    for ts in term_tokenstreams:
        print(f"working on: {''.join([x.text for x in ts])}")
        res: Node = parser_tester(ts, "term")
        indent(res)
        dump(res)
        assert res
        print()
