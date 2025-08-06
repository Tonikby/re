"""
Status bar component for RetroEdit
Shows insert/replace mode, encoding, line endings, filename, cursor position, and modified status
"""

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label
from textual.containers import Horizontal
from pathlib import Path
from typing import Optional
from ..config import config


class StatusBar(Widget):
    """Status bar widget showing editor information"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_path: Optional[Path] = None
        self.cursor_row: int = 0
        self.cursor_col: int = 0
        self.modified: bool = False
        self.encoding: str = "UTF-8"
        
    def compose(self) -> ComposeResult:
        """Create the status bar layout"""
        with Horizontal():
            yield Label("", id="status-info")
    
    def update_status(
        self, 
        file_path: Optional[Path] = None,
        cursor_row: int = 0,
        cursor_col: int = 0,
        modified: bool = False,
        encoding: str = "UTF-8"
    ):
        """Update status bar information"""
        self.file_path = file_path
        self.cursor_row = cursor_row
        self.cursor_col = cursor_col
        self.modified = modified
        self.encoding = encoding.upper()
        
        self._refresh_display()
    
    def _refresh_display(self):
        """Refresh the status bar display"""
        # Insert/Replace mode
        mode = "Insert" if config.insert_mode else "Replace"
        
        # Line ending format
        line_ending = config.line_ending
        
        # Filename
        if self.file_path:
            filename = self.file_path.name
        else:
            filename = "Untitled"
        
        # Cursor position (1-based for display)
        cursor_info = f"Ln {self.cursor_row + 1}, Col {self.cursor_col + 1}"
        
        # Modified indicator
        modified_indicator = " *" if self.modified else ""
        
        # Build status text
        status_text = (
            f" {mode} | {self.encoding} | {line_ending} | {filename} | "
            f"{cursor_info}{modified_indicator}"
        )
        
        # Update the label
        status_label = self.query_one("#status-info", Label)
        status_label.update(status_text)
    
    def on_mount(self) -> None:
        """Called when widget is mounted"""
        self._refresh_display()
    
    def toggle_insert_mode(self) -> None:
        """Toggle between insert and replace mode"""
        config.insert_mode = not config.insert_mode
        self._refresh_display()
    
    def set_encoding(self, encoding: str) -> None:
        """Set the current encoding"""
        self.encoding = encoding.upper()
        self._refresh_display()
    
    def set_line_ending(self, line_ending: str) -> None:
        """Set the line ending format"""
        config.line_ending = line_ending
        self._refresh_display()
