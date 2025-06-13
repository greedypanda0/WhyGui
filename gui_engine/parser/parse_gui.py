import re
import json
from .parse_tags import parse_tags
from .parse_meta import parse_meta

def parse_gui(file_path):
    with open(file_path, 'r') as f:
        raw = f.read()
        
    gui_data = {
        "meta": parse_meta(raw),
        "tree": parse_tags(raw)
    }
    
    return gui_data