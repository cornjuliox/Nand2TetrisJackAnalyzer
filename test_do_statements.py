from typing import List, Iterable, cast
from xml.etree.ElementTree import Element, dump

from utils import make_tokenstream, parser_tester, indent

if __name__ == "__main__":
    sample_do: list[str] = [
        # "do game.run();",
        # "do screen.setcolor(false);",
        # "do screen.drawrectangle(x, y, x + 1, y + size);",
        # "do screen.drawrectangle((x + size) - 1, y, x + size, y + size);",
        "do Output.printInt(sum / length);"
    ]

    do_tokenstreams: List[List[Element]] = [make_tokenstream(x) for x in sample_do]

    for ts in do_tokenstreams:
        working_on: str = ''.join([cast(str, x.text) for x in cast(Iterable[Element], ts)])
        print(f"working on: {working_on}")
        res = parser_tester(ts, "_subroutine_do")
        indent(res)
        dump(res)
        assert res
        print()

    print("finished")
