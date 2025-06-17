import re
import textwrap

def parse_meta(raw):
    pattern = r'@(\w+)\s+(?:"(.*?)"|{(.*?)})'
    matches = re.findall(pattern, raw, re.DOTALL)

    meta = {}
    for key, val, block in matches:
        if block:
            meta[key] = textwrap.dedent(block.strip())
        else:
            meta[key] = val.strip()
    return meta
