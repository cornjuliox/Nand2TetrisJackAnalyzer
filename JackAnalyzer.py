import sys
import os
from typing import List, cast
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree, indent

from Tokenizer import TokenBuilder, RULES
from Token import KEYWORD_LIST
from Parser import JackParser

if __name__ == "__main__":
    dispatch: dict = {
        "tokenize": None,
        "parse": None
    }
    try:
        infile: str = sys.argv[1]
    except IndexError:
        print("usage: JackAnalyzer.py <inputFileOrDirectory>")
        sys.exit()

    inpath: Path = Path(infile)
    for_processing: List[Path] = []
    print(f"-> currently working from {os.getcwd()}")
    if inpath.is_dir():
        print("-> <input> is directory")
        for jackfile in inpath.glob("*.jack"):
            for_processing.append(jackfile)
    else:
        print("-> <input> is a file")
        for_processing.append(inpath)

    print("-> JackAnalyzer v1")
    print(f"-> Analyzing the following files: {for_processing}")

    results: List[tuple] = []
    for filepath in for_processing:
        with filepath.open() as F:
            raw_contents: str = F.read()
        tb: TokenBuilder = TokenBuilder(raw_contents, RULES, KEYWORD_LIST)
        print(f"-> Tokenizing {filepath}.")
        # import pdb
        # pdb.set_trace()
        raw_tokens: List[Element] = [x for x in tb if x is not None]
        print(raw_tokens)
        parser: JackParser = JackParser(tokens=raw_tokens)

        # NOTE: need to prep the token tree for the <file>T.xml file
        token_tree: Element = Element("tokens")
        token_tree.extend(raw_tokens)
        output_token_tree: ElementTree = ElementTree(token_tree)

        # NOTE: and this one is for the main <file>.xml
        class_tree: Element = parser.klass()
        output_parse_tree: ElementTree = ElementTree(class_tree)

        # NOTE: and now we use the built-in write, not the path write
        output_token_file_name: str = f"{filepath.stem}T.xml"
        # NOTE: If you don't use indent() it won't print properly,
        #       everything will end up being on one line.
        indent(output_token_tree)
        output_token_tree.write(output_token_file_name, short_empty_elements=False)

        output_class_file_name: str = f"{filepath.stem}.xml"
        indent(output_parse_tree)
        output_parse_tree.write(output_class_file_name, short_empty_elements=False)
    
    print("-> Program complete!")


