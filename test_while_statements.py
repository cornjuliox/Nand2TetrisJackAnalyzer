from typing import List, Iterable, cast
from xml.etree.ElementTree import indent, Element

from utils import make_tokenstream, parser_tester, dump

if __name__ == "__main__":
    sample_while: list[str] = [
        """
        while (i < length) {
            let a[i] = Keyboard.readInt("ENTER THE NEXT NUMBER: ");
            let i = i + 1;
        }
        """
        """
        while (key = 0) {
            let key = Keyboard.keyPressed();
            do moveSquare();
        }
        """,
        """
        while (exit) {
            while (key) {
            let key = key;
            do moveSquare();
            }

            if (key) { let exit = exit; }
            if (key) { do square.decSize(); }
            if (key) { do square.incSize(); }
            if (key) { let direction = exit; }
            if (key) { let direction = key; }
            if (key) { let direction = square; }
            if (key) { let direction = direction; }

            while (key) {
            let key = key;
            do moveSquare();
            }
        }
        """,
    ]

    while_tokenstreams: List[List[Element]] = [make_tokenstream(x) for x in sample_while] 

    for ts in while_tokenstreams:
        working_on: str = ''.join([cast(str, x.text) for x in cast(Iterable[Element], ts)])
        print(f"working on: {working_on}")
        res: Element = parser_tester(ts, "_subroutine_while")
        indent(res)
        dump(res)
        assert res

    print("finished")

