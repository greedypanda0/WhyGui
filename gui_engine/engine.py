from .parser.parse_gui import parse_gui
from .gui.pyside import pyside_gui

class GUIEngine:
    def __init__(self):
        self.entry_dir = None

    def add_app(self, dir_path: str):
        self.app = pyside_gui()
        self.entry_dir = dir_path

    def run(self):
        if not self.entry_dir:
            raise ValueError("No GUI app directory set.")
        entry_file = f"{self.entry_dir}/App.gui"
        parsed_gui = parse_gui(entry_file)
        print(f"parsed {parsed_gui}")
        self.app.build_from_json(parsed_gui["tree"])
        self.app.run_app()
