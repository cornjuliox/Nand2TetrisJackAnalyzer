from typing import List, Iterable, cast
from xml.etree.ElementTree import indent, Element

from utils import make_tokenstream, parser_tester, dump

if __name__ == "__main__":
    sample_expressions: List[str] = [
        "null",
        "-1",
        "~4",
        "a[2]",
        "i * (-j)",
        "j / (-2)",
        "i | j",
        "someClass.someMethod() + anotherClass.anotherMethod()"
    ]
    expression_tokenstreams: List[List[Element]] = [make_tokenstream(x) for x in sample_expressions] 
    for ts in expression_tokenstreams:
        working_on: str = ''.join([cast(str, x.text) for x in cast(Iterable[Element], ts)])
        print(f"working on: {working_on}")
        res: Element = parser_tester(ts, "expression", debug=True)
        indent(res)
        dump(res)
        print()
        assert res
