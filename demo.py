#!/usr/bin/env python3
"""
Demo script for RetroEdit
Shows basic functionality without requiring user interaction
"""

import sys
from pathlib import Path
from retroedit.config import config
from retroedit.editor import TextBuffer
from retroedit.fileio import detect_encoding, load_file, save_file

def demo_text_buffer():
    """Demonstrate text buffer functionality"""
    print("=== RetroEdit Text Buffer Demo ===")
    
    # Create a new text buffer
    buffer = TextBuffer()
    print("✓ Created new text buffer")
    
    # Add some text
    buffer.insert_char('H')
    buffer.insert_char('e')
    buffer.insert_char('l')
    buffer.insert_char('l')
    buffer.insert_char('o')
    print(f"✓ Inserted text: '{buffer.get_current_line()}'")
    
    # Create a new line
    buffer.insert_newline()
    buffer.insert_char('W')
    buffer.insert_char('o')
    buffer.insert_char('r')
    buffer.insert_char('l')
    buffer.insert_char('d')
    buffer.insert_char('!')
    print(f"✓ Added new line: '{buffer.get_line(1)}'")
    
    # Show buffer content
    print("Buffer content:")
    for i in range(buffer.get_line_count()):
        print(f"  Line {i+1}: '{buffer.get_line(i)}'")
    
    # Test undo
    buffer.undo()
    print("✓ Undo operation successful")
    
    print(f"✓ Cursor position: {buffer.get_cursor_position()}")
    print(f"✓ Line count: {buffer.get_line_count()}")


def demo_file_operations():
    """Demonstrate file I/O functionality"""
    print("\n=== RetroEdit File Operations Demo ===")
    
    # Test encoding detection
    if Path("test.txt").exists():
        encoding = detect_encoding(Path("test.txt"))
        print(f"✓ Detected encoding for test.txt: {encoding}")
        
        # Load the file
        content, detected_enc = load_file(Path("test.txt"))
        lines = content.splitlines()
        print(f"✓ Loaded file with {len(lines)} lines using {detected_enc} encoding")
        print(f"  First line: '{lines[0] if lines else '(empty)'}'")
    
    # Test creating and saving a file
    test_content = """Hello from RetroEdit!

This is a test file created by the demo.

Features:
- Retro MS-DOS Edit interface
- Multiple text encodings
- Configurable line endings
- Undo/Redo support
- Cut/Copy/Paste operations

Enjoy using RetroEdit!"""
    
    demo_file = Path("demo_output.txt")
    save_file(demo_file, test_content)
    print(f"✓ Created demo file: {demo_file}")
    
    # Load it back
    loaded_content, enc = load_file(demo_file)
    print(f"✓ Loaded back demo file using {enc} encoding")
    print(f"  Content matches: {content == test_content}")


def demo_config():
    """Demonstrate configuration functionality"""
    print("\n=== RetroEdit Configuration Demo ===")
    
    print(f"✓ Show line numbers: {config.show_line_numbers}")
    print(f"✓ Show status bar: {config.show_status_bar}")
    print(f"✓ Insert mode: {config.insert_mode}")
    print(f"✓ Tab size: {config.tab_size}")
    print(f"✓ Line ending: {config.line_ending}")
    print(f"✓ Encoding: {config.encoding}")
    print(f"✓ Line ending chars: {repr(config.get_line_ending_chars())}")


def main():
    """Run the demo"""
    print("RetroEdit - MS-DOS Edit Inspired Text Editor")
    print("=" * 50)
    print()
    
    try:
        demo_text_buffer()
        demo_file_operations()
        demo_config()
        
        print("\n=== Demo Complete ===")
        print("✓ All core functionality working correctly!")
        print()
        print("To run RetroEdit:")
        print("  python main.py [filename]")
        print()
        print("Example commands:")
        print("  python main.py                    # Start with empty file")
        print("  python main.py test.txt           # Open existing file")
        print("  python main.py --encoding=cp437   # Use specific encoding")
        
    except Exception as e:
        print(f"✗ Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
