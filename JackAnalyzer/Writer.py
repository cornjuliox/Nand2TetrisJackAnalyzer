from typing import List

from Token import Token

def token_fucker(token: Token) -> str:
    template: str = "<{}>{}</{}>"
    tag: str = token.type.lower()
    value: str = token.value
    xml_tag: str = template.format(tag, value, tag)
    return xml_tag

def xml_fucker(tokens: List[str]) -> str:
    template: str = "<tokens>\n{}\n</tokens>"
    tags: str = "\n".join(tokens)
    final: str = template.format(tags)
    return final
