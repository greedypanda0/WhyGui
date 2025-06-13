import re


def parse_object_block(block):
    kv_item_pattern = re.compile(r"(\w+)\s*\[\s*(.*?)\s*\]", re.DOTALL)
    result = {}

    for k, v in kv_item_pattern.findall(block.strip()):
        res = v.strip()

        if res == "false":
            res = False
        elif res == "true":
            res = True
        elif res.isdigit():
            res = int(res)

        result[k] = v.strip()

    return result


def parse_props(raw_props):
    props = {}
    i = 0
    length = len(raw_props)
    key_match = re.match(r"(\w+)\s*=", raw_props)

    while i < length:
        while i < length and raw_props[i] in " \n\t":
            i += 1
        if i >= length:
            break

        key_match = re.match(r"(\w+)\s*=", raw_props[i:])
        if not key_match:
            break

        key = key_match.group(1)
        i += key_match.end()

        if i < length and raw_props[i] == "{":
            i += 1
            depth = 1
            value = ""
            while i < length and depth > 0:
                if raw_props[i] == "{":
                    depth += 1
                elif raw_props[i] == "}":
                    depth -= 1
                if depth > 0:
                    value += raw_props[i]
                i += 1

            props[key] = parse_object_block(value)

        elif i < length and raw_props[i] == '"':
            i += 1
            value = ""
            while i < length and raw_props[i] != '"':
                value += raw_props[i]
                i += 1
            i += 1
            props[key] = value

        else:
            value = ""
            while i < length and raw_props[i] not in " \n\t":
                value += raw_props[i]
                i += 1
            if value == "true":
                value = True
            elif value == "false":
                value = False
            elif value.isdigit():
                value = int(value)

            props[key] = value

    return props
