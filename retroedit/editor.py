"""
Core editor functionality for RetroEdit
Handles text buffer, cursor navigation, and text operations
"""

from typing import List, Tuple, Optional
from pathlib import Path
from .config import config
from .fileio import load_file, save_file


class TextBuffer:
    """Text buffer with undo/redo support"""
    
    def __init__(self):
        self.lines: List[str] = [""]
        self.cursor_row: int = 0
        self.cursor_col: int = 0
        self.modified: bool = False
        self.file_path: Optional[Path] = None
        self.encoding: str = "utf-8"
        
        # Undo/Redo stacks (simple implementation)
        self.undo_stack: List[Tuple[List[str], int, int]] = []
        self.redo_stack: List[Tuple[List[str], int, int]] = []
        
        # Selection
        self.selection_start: Optional[Tuple[int, int]] = None
        self.selection_end: Optional[Tuple[int, int]] = None
        
        # Find/Replace
        self.last_search: str = ""
        self.last_replace: str = ""
    
    def save_state(self):
        """Save current state for undo"""
        if len(self.undo_stack) > 50:  # Limit undo history
            self.undo_stack.pop(0)
        
        self.undo_stack.append((
            [line for line in self.lines],  # Deep copy of lines
            self.cursor_row,
            self.cursor_col
        ))
        self.redo_stack.clear()  # Clear redo stack when new action is performed
    
    def undo(self) -> bool:
        """Undo last operation"""
        if not self.undo_stack:
            return False
        
        # Save current state to redo stack
        self.redo_stack.append((
            [line for line in self.lines],
            self.cursor_row,
            self.cursor_col
        ))
        
        # Restore previous state
        lines, row, col = self.undo_stack.pop()
        self.lines = lines
        self.cursor_row = row
        self.cursor_col = col
        self.modified = True
        
        return True
    
    def redo(self) -> bool:
        """Redo last undone operation"""
        if not self.redo_stack:
            return False
        
        # Save current state to undo stack
        self.undo_stack.append((
            [line for line in self.lines],
            self.cursor_row,
            self.cursor_col
        ))
        
        # Restore redo state
        lines, row, col = self.redo_stack.pop()
        self.lines = lines
        self.cursor_row = row
        self.cursor_col = col
        self.modified = True
        
        return True
    
    def load_file(self, file_path: Path, encoding: Optional[str] = None) -> None:
        """Load a file into the buffer"""
        content, detected_encoding = load_file(file_path, encoding)
        
        self.lines = content.splitlines() or [""]
        self.file_path = file_path
        self.encoding = detected_encoding
        self.cursor_row = 0
        self.cursor_col = 0
        self.modified = False
        self.undo_stack.clear()
        self.redo_stack.clear()
    
    def save_file(self, file_path: Optional[Path] = None) -> None:
        """Save the buffer to a file"""
        if file_path is None:
            file_path = self.file_path
        
        if file_path is None:
            raise ValueError("No file path specified")
        
        content = '\n'.join(self.lines)
        save_file(file_path, content, self.encoding)
        
        self.file_path = file_path
        self.modified = False
    
    def get_line_count(self) -> int:
        """Get the number of lines in the buffer"""
        return len(self.lines)
    
    def get_line(self, row: int) -> str:
        """Get a line by row number"""
        if 0 <= row < len(self.lines):
            return self.lines[row]
        return ""
    
    def get_cursor_position(self) -> Tuple[int, int]:
        """Get current cursor position (row, col)"""
        return self.cursor_row, self.cursor_col
    
    def set_cursor_position(self, row: int, col: int) -> None:
        """Set cursor position with bounds checking"""
        self.cursor_row = max(0, min(row, len(self.lines) - 1))
        self.cursor_col = max(0, min(col, len(self.get_current_line())))
    
    def get_current_line(self) -> str:
        """Get the current line where cursor is located"""
        return self.get_line(self.cursor_row)
    
    def move_cursor(self, delta_row: int, delta_col: int) -> None:
        """Move cursor by delta amounts"""
        new_row = self.cursor_row + delta_row
        new_col = self.cursor_col + delta_col
        
        # Handle line boundaries
        if new_row < 0:
            new_row = 0
            new_col = 0
        elif new_row >= len(self.lines):
            new_row = len(self.lines) - 1
            new_col = len(self.get_line(new_row))
        else:
            # Handle column boundaries
            line_length = len(self.get_line(new_row))
            if new_col < 0:
                if new_row > 0:
                    new_row -= 1
                    new_col = len(self.get_line(new_row))
                else:
                    new_col = 0
            elif new_col > line_length:
                if new_row < len(self.lines) - 1:
                    new_row += 1
                    new_col = 0
                else:
                    new_col = line_length
        
        self.set_cursor_position(new_row, new_col)
    
    def insert_char(self, char: str) -> None:
        """Insert a character at cursor position"""
        self.save_state()
        
        current_line = list(self.get_current_line())
        
        if config.insert_mode:
            # Insert mode
            current_line.insert(self.cursor_col, char)
        else:
            # Overwrite mode
            if self.cursor_col < len(current_line):
                current_line[self.cursor_col] = char
            else:
                current_line.append(char)
        
        self.lines[self.cursor_row] = ''.join(current_line)
        self.cursor_col += 1
        self.modified = True
    
    def insert_newline(self) -> None:
        """Insert a new line at cursor position"""
        self.save_state()
        
        current_line = self.get_current_line()
        
        # Split current line at cursor
        left_part = current_line[:self.cursor_col]
        right_part = current_line[self.cursor_col:]
        
        # Update current line and insert new line
        self.lines[self.cursor_row] = left_part
        self.lines.insert(self.cursor_row + 1, right_part)
        
        # Move cursor to beginning of new line
        self.cursor_row += 1
        self.cursor_col = 0
        self.modified = True
    
    def delete_char(self) -> None:
        """Delete character at cursor position (Delete key)"""
        self.save_state()
        
        current_line = self.get_current_line()
        
        if self.cursor_col < len(current_line):
            # Delete character at cursor
            new_line = current_line[:self.cursor_col] + current_line[self.cursor_col + 1:]
            self.lines[self.cursor_row] = new_line
        elif self.cursor_row < len(self.lines) - 1:
            # Delete line break (merge with next line)
            next_line = self.get_line(self.cursor_row + 1)
            self.lines[self.cursor_row] = current_line + next_line
            self.lines.pop(self.cursor_row + 1)
        
        self.modified = True
    
    def backspace(self) -> None:
        """Delete character before cursor (Backspace key)"""
        if self.cursor_col > 0:
            self.cursor_col -= 1
            self.delete_char()
        elif self.cursor_row > 0:
            # Move to end of previous line and merge
            prev_line_length = len(self.get_line(self.cursor_row - 1))
            self.cursor_row -= 1
            self.cursor_col = prev_line_length
            self.delete_char()
    
    def get_selected_text(self) -> str:
        """Get currently selected text"""
        if not self.selection_start or not self.selection_end:
            return ""
        
        start_row, start_col = self.selection_start
        end_row, end_col = self.selection_end
        
        # Ensure start is before end
        if (start_row > end_row) or (start_row == end_row and start_col > end_col):
            start_row, start_col, end_row, end_col = end_row, end_col, start_row, start_col
        
        if start_row == end_row:
            # Single line selection
            return self.get_line(start_row)[start_col:end_col]
        else:
            # Multi-line selection
            result = []
            for row in range(start_row, end_row + 1):
                line = self.get_line(row)
                if row == start_row:
                    result.append(line[start_col:])
                elif row == end_row:
                    result.append(line[:end_col])
                else:
                    result.append(line)
            return '\n'.join(result)
    
    def delete_selected_text(self) -> None:
        """Delete currently selected text"""
        if not self.selection_start or not self.selection_end:
            return
        
        self.save_state()
        
        start_row, start_col = self.selection_start
        end_row, end_col = self.selection_end
        
        # Ensure start is before end
        if (start_row > end_row) or (start_row == end_row and start_col > end_col):
            start_row, start_col, end_row, end_col = end_row, end_col, start_row, start_col
        
        if start_row == end_row:
            # Single line deletion
            line = self.get_line(start_row)
            new_line = line[:start_col] + line[end_col:]
            self.lines[start_row] = new_line
        else:
            # Multi-line deletion
            start_line = self.get_line(start_row)[:start_col]
            end_line = self.get_line(end_row)[end_col:]
            
            # Replace the range with a single line
            self.lines[start_row] = start_line + end_line
            
            # Remove lines in between
            for _ in range(start_row + 1, end_row + 1):
                if start_row + 1 < len(self.lines):
                    self.lines.pop(start_row + 1)
        
        # Set cursor to start of selection
        self.cursor_row = start_row
        self.cursor_col = start_col
        self.selection_start = None
        self.selection_end = None
        self.modified = True
    
    def find_text(self, search_text: str, start_pos: Optional[Tuple[int, int]] = None) -> Optional[Tuple[int, int]]:
        """Find text in buffer starting from given position"""
        if not search_text:
            return None
        
        start_row, start_col = start_pos or (self.cursor_row, self.cursor_col)
        
        # Search from current position to end of buffer
        for row in range(start_row, len(self.lines)):
            line = self.get_line(row)
            col_start = start_col if row == start_row else 0
            
            pos = line.find(search_text, col_start)
            if pos >= 0:
                return (row, pos)
        
        # Search from beginning to current position (wrap around)
        for row in range(0, start_row + 1):
            line = self.get_line(row)
            col_end = start_col if row == start_row else len(line)
            
            pos = line.find(search_text, 0)
            if pos >= 0 and pos < col_end:
                return (row, pos)
        
        return None
    
    def replace_text(self, search_text: str, replace_text: str, replace_all: bool = False) -> int:
        """Replace text in buffer. Returns number of replacements made."""
        if not search_text:
            return 0
        
        replacements = 0
        
        if replace_all:
            # Replace all occurrences
            for row in range(len(self.lines)):
                line = self.lines[row]
                if search_text in line:
                    self.lines[row] = line.replace(search_text, replace_text)
                    replacements += line.count(search_text)
        else:
            # Replace current occurrence
            pos = self.find_text(search_text)
            if pos:
                row, col = pos
                line = self.get_line(row)
                new_line = line[:col] + replace_text + line[col + len(search_text):]
                self.lines[row] = new_line
                replacements = 1
        
        if replacements > 0:
            self.save_state()
            self.modified = True
        
        return replacements
