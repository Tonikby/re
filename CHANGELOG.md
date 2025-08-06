# Changelog

All notable changes to RetroEdit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Find & Replace dialog (planned)
- Go to Line dialog (planned)
- File browser dialogs (planned)
- Mouse support improvements (planned)

## [1.0.0] - 2024-08-06

### Added
- Initial release of RetroEdit
- MS-DOS Edit inspired retro interface
- Menu bar with File, Edit, View, and Help menus
- Status bar showing insert/replace mode, encoding, line endings, filename, cursor position
- Text editing with line numbers support
- Cut, copy, paste operations
- Undo/redo functionality with multi-level support
- File operations (open, save, save as)
- Multiple encoding support (UTF-8, CP437, CP1252, Latin-1)
- Automatic encoding detection using chardet
- Configurable line endings (CR, LF, CRLF)
- Insert/Replace mode toggle
- Keyboard shortcuts for all major operations
- Cross-platform support (Windows, macOS, Linux)
- Textual TUI framework for professional appearance
- Configuration system with JSON-based settings
- Build scripts for PyInstaller and Nuitka
- Comprehensive documentation and examples
- Demo script showing core functionality
- Setup script for pip installation
- MIT license

### Technical Details
- Python 3.10+ support with type hints
- Modular architecture with clean separation of concerns
- Error handling for file operations
- Virtual environment support
- Requirements files for development and production

### Documentation
- Complete README with installation and usage instructions
- Technical requirements specification
- Project summary with implementation details
- Build instructions for standalone binaries
- Keyboard shortcuts reference

## [0.1.0] - 2024-08-06

### Added
- Project structure and initial codebase
- Core text buffer implementation
- Basic file I/O operations
- Configuration framework
- UI component architecture
