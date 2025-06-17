from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
)

from .parse_style import parse_style

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
            child_widget = add_component(self, child)
            layout.addWidget(parse_style(child_widget))
        return container

    elif ctype == "row_block":
        container = QWidget()
        layout = QHBoxLayout()
        container.setLayout(layout)
        container.props = props
        for child in children:
            child_widget = add_component(self, child)
            layout.addWidget(parse_style(child_widget))
        return container
    
    elif ctype == "link":
        btn_text = comp.get("node_value", "Go")
        route = props.get("href", "/")
        print(route)

        link = QPushButton(btn_text)
        link.clicked.connect(lambda: self.render_page(route))
        link.props = props
        return link

    else:
        print(f"Unknown component type: {ctype}")
        unknown = QWidget()
        unknown.props = props
        return unknown