from PySide6.QtGui import QColor, QPalette, QFont
from PySide6.QtCore import QTimer


def parse_style(component):
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
    width = parse_dimension(component, style.get("width"), axis="width")
    height = parse_dimension(component, style.get("height"), axis="height")

    if width is not None or height is not None:
        # Defer resize until after layout is applied
        QTimer.singleShot(0, lambda: apply_deferred_size(component, width, height))

    return component


def parse_dimension(component, value, axis="width"):
    if not value:
        return None

    if isinstance(value, int):
        return value

    if isinstance(value, str):
        value = value.strip()
        if value.endswith("%"):
            percent = int(value[:-1])
            parent = component.parent()
            if parent:
                base = parent.width() if axis == "width" else parent.height()
            else:
                base = 800 if axis == "width" else 600  # fallback defaults

            return int(base * percent / 100)

        elif value.isdigit():
            return int(value)

    return None


def apply_deferred_size(component, width, height):
    if width is not None or height is not None:
        component.setMinimumSize(width or 0, height or 0)
        component.setMaximumSize(width or 10000, height or 10000)
