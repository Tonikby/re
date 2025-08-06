#!/usr/bin/env python3
"""
Basic tests for RetroEdit editor functionality
"""

import unittest
from pathlib import Path
import tempfile
import os

from retroedit.editor import TextBuffer
from retroedit.config import config


class TestTextBuffer(unittest.TestCase):
    """Test cases for TextBuffer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.buffer = TextBuffer()
    
    def test_initial_state(self):
        """Test initial buffer state"""
        self.assertEqual(self.buffer.get_line_count(), 1)
        self.assertEqual(self.buffer.get_line(0), "")
        self.assertEqual(self.buffer.get_cursor_position(), (0, 0))
        self.assertFalse(self.buffer.modified)
    
    def test_insert_char(self):
        """Test character insertion"""
        self.buffer.insert_char('H')
        self.buffer.insert_char('i')
        
        self.assertEqual(self.buffer.get_line(0), "Hi")
        self.assertEqual(self.buffer.get_cursor_position(), (0, 2))
        self.assertTrue(self.buffer.modified)
    
    def test_insert_newline(self):
        """Test newline insertion"""
        self.buffer.insert_char('H')
        self.buffer.insert_char('i')
        self.buffer.insert_newline()
        self.buffer.insert_char('!')
        
        self.assertEqual(self.buffer.get_line_count(), 2)
        self.assertEqual(self.buffer.get_line(0), "Hi")
        self.assertEqual(self.buffer.get_line(1), "!")
        self.assertEqual(self.buffer.get_cursor_position(), (1, 1))
    
    def test_backspace(self):
        """Test backspace functionality"""
        self.buffer.insert_char('H')
        self.buffer.insert_char('i')
        self.buffer.backspace()
        
        self.assertEqual(self.buffer.get_line(0), "H")
        self.assertEqual(self.buffer.get_cursor_position(), (0, 1))
    
    def test_delete_char(self):
        """Test delete character functionality"""
        self.buffer.insert_char('H')
        self.buffer.insert_char('i')
        self.buffer.set_cursor_position(0, 0)
        self.buffer.delete_char()
        
        self.assertEqual(self.buffer.get_line(0), "i")
        self.assertEqual(self.buffer.get_cursor_position(), (0, 0))
    
    def test_undo_redo(self):
        """Test undo/redo functionality"""
        # Insert some text
        self.buffer.insert_char('H')
        self.buffer.insert_char('i')
        
        # Undo
        result = self.buffer.undo()
        self.assertTrue(result)
        
        # Check state after undo
        self.assertEqual(self.buffer.get_line(0), "H")
        
        # Redo
        result = self.buffer.redo()
        self.assertTrue(result)
        
        # Check state after redo
        self.assertEqual(self.buffer.get_line(0), "Hi")
    
    def test_cursor_movement(self):
        """Test cursor movement"""
        self.buffer.insert_char('H')
        self.buffer.insert_char('e')
        self.buffer.insert_char('l')
        self.buffer.insert_char('l')
        self.buffer.insert_char('o')
        
        # Move cursor
        self.buffer.move_cursor(0, -2)
        self.assertEqual(self.buffer.get_cursor_position(), (0, 3))
        
        # Move cursor to beginning
        self.buffer.move_cursor(0, -10)
        self.assertEqual(self.buffer.get_cursor_position(), (0, 0))
    
    def test_file_operations(self):
        """Test file loading and saving"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Hello\nWorld\n")
            temp_path = Path(f.name)
        
        try:
            # Load the file
            self.buffer.load_file(temp_path)
            
            self.assertEqual(self.buffer.get_line_count(), 2)
            self.assertEqual(self.buffer.get_line(0), "Hello")
            self.assertEqual(self.buffer.get_line(1), "World")
            self.assertFalse(self.buffer.modified)
            
            # Modify and save - move to end of first line
            self.buffer.set_cursor_position(0, 5)  # End of "Hello"
            self.buffer.insert_char('!')
            self.buffer.save_file()
            
            # Load again to verify save
            new_buffer = TextBuffer()
            new_buffer.load_file(temp_path)
            self.assertEqual(new_buffer.get_line(0), "Hello!")
            
        finally:
            # Clean up
            if temp_path.exists():
                os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
