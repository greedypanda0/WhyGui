import sys
from .add_component import add_component
from .parse_style import parse_style
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from .parse_code import eval_code

class pyside_gui:
    def __init__(self, watch_dog):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.resize(800, 600)
        self.window.setWindowTitle("WhyGUI")
        self.watch_dog = watch_dog
        self.runtime_props = {}

        # outer layout
        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)
        print(self.window.size())

    def init(self):
        print("helooooo")
        self.render_page("/")
        self.run_app()

    def build_from_json(self, data):
        for node in data:
            widget = add_component(self, node)
            styled_widget = parse_style(widget)
            self.layout.addWidget(styled_widget)

    def run_app(self):
        self.window.show()
        self.app.exec()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

    def render_page(self, path):
        self.clear_layout(self.layout)
        data = self.watch_dog.get_data(path)

        tree = data.get("tree")
        meta = data.get("meta")
        
        print(meta)
        self.app_path = path
        
        if meta.get("code"):
            eval_code(meta["code"], self.runtime_props)
            
        if meta.get("title"):
            self.window.setWindowTitle(meta["title"])

        if meta.get("height") and meta.get("width"):
            self.window.resize(meta["width"], meta["height"])
    
        self.build_from_json(tree)
