# Contributing to RetroEdit

Thank you for considering contributing to RetroEdit! We welcome contributions from everyone.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct. Please be respectful and considerate to other contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the [Issues](https://github.com/Tonikby/re/issues)
2. If not, create a new issue using the bug report template
3. Provide as much detail as possible, including steps to reproduce the issue

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue using the feature request template
3. Describe the feature and explain why it would be useful

### Code Contributions

1. Fork the repository
2. Create a new branch for your feature/fix: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test your changes thoroughly
5. Run the demo script to ensure everything works: `python demo.py`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/yourusername/re.git
cd re
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Run tests to ensure everything works:
```bash
python demo.py
python -c "from retroedit.app import RetroEditApp; print('Import successful')"
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write clear, descriptive commit messages
- Add comments for complex logic
- Keep functions and classes focused and reasonably sized

## Testing

- Test your changes on multiple platforms if possible (Windows, macOS, Linux)
- Ensure the demo script runs without errors
- Test with different Python versions (3.10, 3.11, 3.12)
- Verify that the application launches and basic functionality works

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Update documentation if necessary
3. Add tests for new functionality
4. Ensure all tests pass
5. Update the README.md if needed
6. Fill out the pull request template completely

## Areas for Contribution

### High Priority
- Find & Replace dialog implementation
- Go to Line dialog
- File browser dialogs
- Save confirmation dialogs
- Unit tests

### Medium Priority
- Mouse support improvements
- Syntax highlighting for common file types
- Word wrap functionality
- Advanced search features (regex)

### Low Priority
- Command palette (Ctrl+P)
- Bookmarks system
- Split view editing
- Alternative themes
- Plugin system

## Project Structure

```
retroedit/
├── main.py                    # Entry point
├── retroedit/
│   ├── app.py                # Main application
│   ├── editor.py             # Text buffer
│   ├── config.py             # Configuration
│   ├── fileio.py             # File operations
│   ├── utils.py              # Utilities
│   └── ui/                   # UI components
├── requirements.txt          # Dependencies
├── setup.py                  # Package setup
└── docs/                     # Documentation
```

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the question label
- Start a discussion in the Discussions tab
- Contact the maintainers

Thank you for helping make RetroEdit better! 🎉
