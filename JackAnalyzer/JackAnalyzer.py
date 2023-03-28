import sys
import os
from typing import List
from pathlib import Path

from JackAnalyzer.Tokenizer import TokenBuilder, RULES
from JackAnalyzer.Token import KEYWORD_LIST
from JackAnalyzer.Writer import token_fucker, xml_fucker
from JackAnalyzer.OldParser import JackParser

if __name__ == "__main__":
    try:
        infile: str = sys.argv[1]
    except IndexError:
        print("usage: JackAnalyzer.py <inputFileOrDirectory>")
        sys.exit()

    inpath: Path = Path(infile)
    for_processing: List[str] = []
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
            raw_contents: List[str] = F.read()

        contents: str = raw_contents

        tb: TokenBuilder = TokenBuilder(contents, RULES, KEYWORD_LIST)
        print(f"-> Tokenizing {filepath}.")
        tokens: List[tuple] = [x for x in tb if x]
        print(tokens)
        parser: JackParser = JackParser(tokens=tokens)
    
    print("-> Program complete!")


