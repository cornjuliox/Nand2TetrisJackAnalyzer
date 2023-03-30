from typing import List, Iterable, cast
from xml.etree.ElementTree import indent, dump, Element

from utils import make_tokenstream, parser_tester

if __name__ == "__main__":
    sample_class_var_dec: List[str] = [
        "field int x, y; // screen location of the square's top-left corner",
        "field int size; // length of this square, in pixels",
        "static boolean test;",
        "field Square square; // the square of this game",
        "field int direction;",
    ]
    sample_class_var_dec_tokenstreams: List[List[Element]] = [make_tokenstream(x) for x in sample_class_var_dec]

    for ts in sample_class_var_dec_tokenstreams:
        working_on: str = ''.join([cast(str, x.text) for x in cast(Iterable[Element], ts)])
        print(f"working on: {working_on}")
        res = parser_tester(ts, "klass_var_dec")
        indent(res)
        dump(res)
        assert res
    print("finished")

