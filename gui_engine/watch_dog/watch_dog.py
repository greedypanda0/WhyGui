import os
import json
from ..parser.parse_gui import parse_gui  # make sure __init__.py exists in folders


class watch_dog:
    def __init__(self, config):
        self.config = config
        self.component_map = {}

    def init(self):
        self.walk_app()

        return True

    def walk_app(self):
        for root, dirs, files in os.walk(self.config.app_dir):
            for file in files:
                if file.endswith(".gui"):
                    file_path = os.path.join(root, file)
                    parsed_gui = parse_gui(file_path)
                    self.create_file(file_path, parsed_gui)

    def read_file(self, file_path):
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print(f"[!] JSON parsing failed for {file_path}: {e}")
                return None

    def get_data(self, name):
        data_path = self.component_map.get(name)
        return self.read_file(data_path)

    def create_file(self, file_path, data):
        rel_path = os.path.relpath(file_path, self.config.app_dir)

        if rel_path.endswith(".gui"):
            rel_path = rel_path[:-3] + "json"
        else:
            rel_path = rel_path + ".json"

        full_output_path = os.path.join(".whygui", rel_path)
        if data.get("meta", {}).get("page"):
            self.component_map[data["meta"]["page"]] = full_output_path

        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)

        with open(full_output_path, "w") as f:
            if isinstance(data, (dict, list)):
                f.write(json.dumps(data, indent=2))
            else:
                f.write(str(data))
