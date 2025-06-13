import re
def parse_meta(raw):
    pattern = r'@(\w+)(?:\s+"(.*?)"|)\s*(?:{(.*?)}|)'
    matches = re.findall(pattern, raw, re.DOTALL)

    meta = {}
    for name, val, block in matches:
        if block:
            meta[name] = block.strip()
        elif val:
            meta[name] = val.strip()
            
    return meta