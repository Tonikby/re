# RetroEdit

A retro-style text editor inspired by MS-DOS Edit, built with Python and Textual.

## Features

- **Retro Interface**: MS-DOS Edit inspired UI with classic color scheme
- **Menu Bar**: File, Edit, View, and Help menus with keyboard navigation  
- **Status Bar**: Shows insert/replace mode, encoding, line endings, filename, cursor position, and modified status
- **Line Numbers**: Optional line number display
- **Text Operations**: Cut, copy, paste, undo, redo
- **Find & Replace**: Search and replace functionality (planned)
- **Multiple Encodings**: Support for UTF-8, CP437, CP1252, Latin-1
- **Configurable Line Endings**: CR, LF, or CRLF
- **Cross-Platform**: Runs on Windows, macOS, and Linux

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/example/retroedit.git
cd retroedit
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py [filename]
```

### Using pip (when published):
```bash
pip install retroedit
retroedit [filename]
```

## Usage

### Command Line
```bash
# Start with empty file
retroedit

# Open an existing file
retroedit myfile.txt

# Open with specific encoding
retroedit --encoding=cp437 myfile.txt
```

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New file | Ctrl+N |
| Open file | Ctrl+O |
| Save file | Ctrl+S |
| Save As | F2 |
| Exit | Ctrl+Q |
| Undo | Ctrl+Z |
| Redo | Ctrl+Y |
| Cut | Ctrl+X |
| Copy | Ctrl+C |
| Paste | Ctrl+V |
| Find | Ctrl+F |
| Replace | Ctrl+R |
| Go to Line | Ctrl+G |
| Toggle Insert/Replace | Insert |
| Help | F1 |
| Menu | F10 |

### Menu Navigation

- Use **Alt + [letter]** to access menus (e.g., Alt+F for File menu)
- Use **F10** to activate menu bar
- Use **Arrow keys** to navigate menus
- Press **Enter** to select menu items
- Press **Esc** to cancel menu operations

## Building Binaries

### Using PyInstaller:
```bash
pyinstaller --onefile --console main.py --name retroedit
```

### Using Nuitka:
```bash
nuitka --onefile --console main.py --output-filename=retroedit
```

## Configuration

RetroEdit saves configuration in JSON format. Settings include:
- Line numbers visibility
- Status bar visibility
- Tab size and spaces vs tabs
- Default encoding
- Line ending preference
- Color scheme options

## Architecture

RetroEdit is built using a modular architecture:

- `main.py` - Application entry point
- `retroedit/app.py` - Main application class
- `retroedit/editor.py` - Text buffer and editing operations
- `retroedit/config.py` - Configuration management
- `retroedit/fileio.py` - File I/O with encoding support
- `retroedit/ui/` - User interface components
  - `menu.py` - Menu bar
  - `status.py` - Status bar
  - `text_editor.py` - Text editing widget
- `retroedit/utils.py` - Utility functions

## Technical Details

- **Language**: Python 3.10+
- **UI Framework**: Textual (Rich-based TUI)
- **Encoding Detection**: chardet library
- **Packaging**: PyInstaller or Nuitka for standalone binaries

## Development Status

RetroEdit is currently in beta. Core functionality is implemented:

✅ Basic text editing
✅ File operations (open, save)
✅ Menu system
✅ Status bar
✅ Undo/redo
✅ Cut/copy/paste
✅ Retro styling
✅ Encoding support

🚧 Planned features:
- Find & Replace dialogs
- Go to Line dialog
- File browser dialog
- Mouse support
- Syntax highlighting
- Command palette

## Contributing

Contributions welcome! Please feel free to submit pull requests or open issues.

## License

MIT License - see LICENSE file for details.

## Screenshot

```
┌─[File]──[Edit]──[View]──[Help]──────────────────────────────────────────────┐
│01 │ def main():                                                              │
│02 │     print("Hello, RetroEdit!")                                           │
│03 │                                                                          │
│04 │ # Cursor here...                                                         │
│   │                                                                          ▓
│   │                                                                          ▓
│   │                                                                          ░
│ Insert | UTF-8 | CRLF | example.py | Ln 4, Col 5 | *                        │
└──────────────────────────────────────────────────────────────────────────────┘
```
