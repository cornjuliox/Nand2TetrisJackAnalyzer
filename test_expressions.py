from typing import List
from JackAnalyzer.Token import Token, Node
from xml.etree.ElementTree import indent

from utils import make_tokenstream, parser_tester, dump

if __name__ == "__main__":
    sample_expressions: List[str] = [
        # "null",
        # "-1",
        # "~4",
        # "a[2]",
        # "i * (-j)",
        # "j / (-2)",
        # "i | j",
        "someClass.someMethod() + anotherClass.anotherMethod()"
    ]
    expression_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_expressions] 
    for ts in expression_tokenstreams:
        print(f"working on: {''.join([x.text for x in ts])}")
        res: Node = parser_tester(ts, "expression", debug=True)
        indent(res)
        dump(res)
        print()
        assert res
