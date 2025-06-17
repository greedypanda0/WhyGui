import re
import textwrap
import textwrap

def force_dedent(code):
    lines = code.strip().splitlines()
    if lines and not lines[0].startswith(" ") and any(line.startswith("    ") for line in lines[1:]):
        lines[0] = "    " + lines[0]
    # Join and dedent
    return textwrap.dedent("\n".join(lines))


def eval_code(code, runtime_props):
    clean_code = force_dedent(code)
    exec(clean_code, runtime_props)
    
def evaluate_string(s: str, scope: dict):
    pattern = r"{([^}]+)}"
    return re.sub(pattern, lambda m: str(eval(m.group(1), scope)), s)