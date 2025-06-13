# WhyGUI (IN DEVELOPMENT)

**WhyGUI** is a minimal, custom GUI framework inspired by JSX, XML, and templating engines — but with zero HTML or CSS.

Write simple `.gui` files using a declarative, tag-based syntax and render native desktop UIs using PySide6 (Qt). Perfect for designing rapid prototypes or dynamic UIs with full Python control.

---

## 🧩 Features

- 📄 Custom `.gui` file format
- 🧠 Smart parser that turns tags into component trees
- 🎨 Inline styling via `style={ key[value] ... }`
- ⚙️ Metadata with `@title`, `@page`, and `@code` blocks
- 🪟 Built on PySide6 for native GUI rendering
- 🔥 No web technologies involved — pure Python

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install PySide6
```

```
# App.gui

@title "home"
@page "/"
@code {
    print("hello from code block")
}

<column_block style={ background[#ffeeee] width[100%] height[100%] }>
    <row_block style={ background[#ddf] height[60] }>
        <text style={ text[My GUi] font_size[24] background[#cce] }></text>
    </row_block>
    <column_block style={ background[#fefefe] height[200] }>
        <text style={ text[Welcome to the test!] font_size[16] }></text>
    </column_block>
</column_block>
```

```bash
python main.py
```

## Progress
- parsing [done]
- multiple page support [in progress]
- css support [in progress]
- code support
- local storage support
- and more ...

---

its open to contributions!!!! or pls contribute lol