from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
)

from .parse_style import parse_style
from .parse_code import evaluate_string


def add_component(self, comp):
    ctype = comp["tag"]
    props = comp.get("props", {})
    children = comp.get("children", [])
    runtime = self.runtime_props  # grab context
    print(runtime)

    def apply_style(widget):
        # Evaluate style["text"] if it exists
        style = props.get("style", {})
        if "text" in style:
            style["text"] = evaluate_string(style["text"], runtime)
        return parse_style(widget)

    if ctype == "text":
        raw_text = comp.get("node_value", "")
        eval_text = evaluate_string(raw_text, runtime)
        label = QLabel(eval_text)
        label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        label.props = props
        return apply_style(label)

    elif ctype == "button":
        raw_text = children if isinstance(children, str) else "Click Me"
        eval_text = evaluate_string(raw_text, runtime)
        btn = QPushButton(eval_text)

        onclick = props.get("onclick")
        if onclick and onclick.startswith("{") and onclick.endswith("}"):
            func_name = onclick[1:-1]
            func = runtime.get(func_name)
            if callable(func):
                btn.clicked.connect(func)
            else:
                print(f"[WARN] No callable '{func_name}' in runtime.")

        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn.props = props
        return apply_style(btn)

    elif ctype == "link":
        raw_text = comp.get("node_value", "Go")
        eval_text = evaluate_string(raw_text, runtime)
        route = props.get("href", "/")

        link = QPushButton(eval_text)
        link.clicked.connect(lambda: self.render_page(route))
        link.props = props
        return apply_style(link)

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

    else:
        print(f"[WARN] Unknown component type: {ctype}")
        unknown = QWidget()
        unknown.props = props
        return unknown
