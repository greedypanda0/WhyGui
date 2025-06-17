from .parser.parse_gui import parse_gui
from .gui.pyside import pyside_gui
from .watch_dog.watch_dog import watch_dog

class GUIEngine:
    def __init__(self):
        self.app_dir = None

    def add_app(self, dir_path: str):
        self.watch_dog = watch_dog(self)
        self.app = pyside_gui(self.watch_dog)
        
        self.app_dir = dir_path

    def run(self):
        if not self.app_dir:
            raise ValueError("No GUI app directory set.")
        
        self.watch_dog.init()
        self.app.init()
