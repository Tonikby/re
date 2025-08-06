
# re (RetroEdit) - Technical Requirements

## Overview

**re** is a command-line text editor inspired by the classic **MS-DOS Edit**, but implemented in **Python**, targeting modern terminal environments. It provides essential text editing features with a retro, menu-driven interface. The project will be compiled to **standalone binaries** for **Windows** and **macOS** using tools like **PyInstaller** or **Nuitka**.

---

## 1. Goals

- Emulate the look and feel of **MS-DOS Edit**
- Provide basic editing functionality in **text-mode terminal**
- Use Python and cross-platform libraries
- Deliver a **menu bar**, **status bar**, **line numbers**, and **scroll bar**
- Keep the functionality **simple and usable**
- Compile into **single binary** executable for Windows and macOS

---

## 2. Technology Stack

| Component            | Choice                          |
|---------------------|----------------------------------|
| Programming Language | Python 3.10+                     |
| TUI Library          | `urwid` or `textual` or `prompt_toolkit` |
| Encoding Support     | `chardet`, `codecs`, `iconv` (if needed) |
| Packaging            | `PyInstaller` or `Nuitka`       |
| Platform Support     | Windows (CMD, PowerShell), macOS (Terminal) |
| License              | MIT or Apache-2.0                |

---

## 3. User Interface Components

### Menu Bar

```
┌─[File]──[Edit]──[View]──[Help]──────────────────────────────────────────────┐
```

- **Keyboard Navigation**: Use `Alt` + Key or arrow keys
- Submenus opened via Enter or right arrow
- Dismiss via Esc or left arrow

### Status Bar

```
│ Insert | UTF-8 | CRLF | myfile.txt | Ln 23, Col 5 | *                      │
```

- **Insert/Replace Mode** toggle
- **Encoding (Code Page)** display
- **Line Ending** format (CR/LF/CRLF)
- **Filename**
- **Cursor position**
- **Modified** indicator (`*`)

### Line Numbers and Scrollbar

```
23 │ This is a line of text...                                  │
24 │ Another line...                                            ▓
25 │ ...                                                        ▓
   │                                                            ░
```

- Line numbers aligned left
- Scrollbar right (visual, optionally interactive)

---

## 4. Core Features

### File Operations
- Open file (`Ctrl+O`)
- Save (`Ctrl+S`)
- Save As (`Ctrl+Shift+S`)
- Exit (`Ctrl+Q`)

### Text Editing
- Insert/overwrite mode toggle (`Insert`)
- Text selection (Shift + arrows)
- Cut / Copy / Paste (`Ctrl+X`, `Ctrl+C`, `Ctrl+V`)
- Undo / Redo (single-level) (`Ctrl+Z`, `Ctrl+Y`)
- Find / Replace (`Ctrl+F`, `Ctrl+R`)
- Goto Line (`Ctrl+G`)

---

## 5. View Options

Accessible from `View → Status Bar Settings`

| Option            | Description                                     |
|------------------|-------------------------------------------------|
| **Line Endings** | CR, LF, or CRLF                                 |
| **Code Page**     | UTF-8, CP437, CP1252, etc.                      |
| **Tab Mode**      | Tabs vs. spaces (e.g., 4 spaces per tab)       |
| **Toggle Status Bar** | Show/hide status bar                     |
| **Toggle Line Numbers** | Show/hide left line numbers            |

---

## 6. Architecture

### Modules

| Module             | Responsibilities                              |
|-------------------|------------------------------------------------|
| `main.py`         | Launch application, init layout                |
| `editor.py`       | Text buffer, navigation, insert/edit/delete    |
| `ui/menu.py`      | Menu bar and input handling                    |
| `ui/status.py`    | Status bar drawing and updates                 |
| `ui/scroll.py`    | Scroll bar rendering and tracking              |
| `config.py`       | Store view options, encoding, tab size         |
| `fileio.py`       | File loading/saving, encoding conversion       |
| `utils.py`        | Helper functions (e.g., replace, find)         |

---

## 7. Encoding Support

- **Default**: UTF-8
- Detect encoding on open using `chardet`
- Allow user to reopen file with selected encoding
- Supported: UTF-8, CP437, CP1252, Latin-1

---

## 8. Build & Packaging

### For Windows/macOS:
- Compile using **PyInstaller**:
  ```bash
  pyinstaller --onefile --console retroedit.py
  ```
- Alternative: Use **Nuitka** for better performance

---

## 9. Keyboard Shortcuts

| Action              | Shortcut       |
|---------------------|----------------|
| Open File           | Ctrl+O         |
| Save File           | Ctrl+S         |
| Save As             | F2             |
| Exit                | Ctrl+Q         |
| Copy / Cut / Paste  | Ctrl+C/X/V     |
| Undo / Redo         | Ctrl+Z / Ctrl+Y|
| Find / Replace      | Ctrl+F / Ctrl+R|
| Goto Line           | Ctrl+G         |
| Toggle Insert Mode  | Insert         |
| Navigate Menu       | Alt + Key      |

---

## 10. Stretch Goals (Optional)

- Basic syntax highlighting (e.g., for `.py`, `.txt`, `.md`)
- Mouse support (selection, scrollbar interaction)
- Command palette (`Ctrl+P`)
- Bookmarks for quick navigation

---

## 11. Risks and Constraints

- Terminal limitations on Windows may require fallback handling
- Non-UTF encodings can be complex — CP conversion must be tested
- UI performance with long files needs profiling

---

## 12. Deliverables

- Python source code
- Build scripts for Windows and macOS
- Sample configuration file (optional)
- README with usage instructions and screenshots

---

## 13. License

- Open-source license: MIT or Apache-2.0

---

## 14. Example Screenshot (Text-based)

```
┌─[File]──[Edit]──[View]──[Help]──────────────────────────────────────────────┐
01 │ def main():                                                              │
02 │     print("Hello, RetroEdit!")                                           │
03 │                                                                          │
04 │ # Cursor here...                                                         │
   │                                                                          ▓
   │                                                                          ▓
   │                                                                          ░
│ Insert | UTF-8 | CRLF | myscript.py | Ln 4, Col 5 | *                      │
```
