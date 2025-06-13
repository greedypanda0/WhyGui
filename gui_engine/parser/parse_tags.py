import re
from .parse_props import parse_props


def clean_tree(tree):
    for item in tree:
        item.pop("__start", None)
        if "children" in item:
            clean_tree(item["children"])

    return tree


def parse_tags(raw):
    tag_pattern = re.compile(r"<(/?\w+)([^>]*)>", re.MULTILINE)
    matches = list(tag_pattern.finditer(raw))
    tree = []
    blocks = []

    last_index = 0
    for match in matches:
        full_tag = match.group(0)
        tag_name = match.group(1)
        raw_props = match.group(2)
        start, end = match.span()
        is_closing = tag_name.startswith("/")
        clean_tag = tag_name.lstrip("/")

        if not is_closing:
            tag = {"tag": clean_tag, "props": parse_props(raw_props), "children": []}

            if blocks:
                prev_end = matches[matches.index(match) - 1].end()
                content_between = raw[prev_end:start].strip()
                if content_between and not content_between.startswith("<"):
                    blocks[-1]["children"][-1]["node_value"] = content_between

            if blocks:
                blocks[-1]["children"].append(tag)
            else:
                tree.append(tag)
            blocks.append(tag)

        else:
            if blocks and blocks[-1]["tag"] == clean_tag:
                inner_text = raw[blocks[-1]["__start"] : start].strip()
                if (
                    inner_text
                    and not inner_text.startswith("<")
                    and not blocks[-1].get("children")
                ):
                    blocks[-1]["node_value"] = inner_text
                blocks.pop()

            else:
                print(f"Invalid tag : </{clean_tag}>")

        if not is_closing and "__start" not in tag:
            tag["__start"] = end

    return clean_tree(tree)
