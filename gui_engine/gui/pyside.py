import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
)
from PySide6.QtGui import QColor, QPalette, QFont


class pyside_gui:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)
        self.window.resize(800, 600)
        self.window.setWindowTitle("WhyGUI")

    def build_from_json(self, data):
        for node in data:
            widget = self.add_component(node)
            styled_widget = self.parse_style(widget)
            self.layout.addWidget(styled_widget)
        self.window.show()

    def add_component(self, comp):
        ctype = comp["tag"]
        props = comp.get("props", {})
        children = comp.get("children", [])

        if ctype == "text":
            label = QLabel(comp.get("node_value", ""))
            label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
            label.props = props
            return label

        elif ctype == "button":
            btn_text = children if isinstance(children, str) else "Click Me"
            btn = QPushButton(btn_text)
            btn.clicked.connect(lambda: print("Button clicked!"))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.props = props
            return btn

        elif ctype == "column_block":
            container = QWidget()
            layout = QVBoxLayout()
            container.setLayout(layout)
            container.props = props
            for child in children:
                child_widget = self.add_component(child)
                layout.addWidget(self.parse_style(child_widget))
            return container

        elif ctype == "row_block":
            container = QWidget()
            layout = QHBoxLayout()
            container.setLayout(layout)
            container.props = props
            for child in children:
                child_widget = self.add_component(child)
                layout.addWidget(self.parse_style(child_widget))
            return container

        else:
            print(f"Unknown component type: {ctype}")
            unknown = QWidget()
            unknown.props = props
            return unknown

    def parse_style(self, component):
        style = component.props.get("style", {})

        if not isinstance(style, dict):
            return component

        # Background color
        if "background" in style:
            color = QColor(style["background"])
            palette = component.palette()
            palette.setColor(QPalette.Window, color)
            component.setAutoFillBackground(True)
            component.setPalette(palette)

        # Text override
        if "text" in style and hasattr(component, "setText"):
            component.setText(str(style["text"]))

        # Font size
        if "font_size" in style:
            font = component.font()
            font.setPointSize(int(style["font_size"]))
            component.setFont(font)

        # Width and height
        width = self.parse_dimension(style.get("width"), axis="width")
        height = self.parse_dimension(style.get("height"), axis="height")

        if width is not None or height is not None:
            component.setMinimumSize(width or 0, height or 0)
            component.setMaximumSize(width or 10000, height or 10000)

        return component

    def parse_dimension(self, value, axis="width"):
        if not value:
            return None

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            value = value.strip()
            if value.endswith("%"):
                percent = int(value[:-1])
                base = (
                    self.window.size().width()
                    if axis == "width"
                    else self.window.size().height()
                )
                return int(base * percent / 100)
            elif value.isdigit():
                return int(value)

        return None

    def run_app(self):
        self.app.exec()
