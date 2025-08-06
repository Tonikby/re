"""
Text editor widget for RetroEdit
Main text editing area with line numbers and scrolling support
"""

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import TextArea
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from textual.message import Message
from rich.text import Text
from rich.syntax import Syntax
from typing import Optional
from pathlib import Path
from ..editor import TextBuffer
from ..config import config


class EditorUpdate(Message):
    """Message sent when editor content changes"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TextEditor(Widget):
    """Text editor widget with line numbers and scrolling"""
    
    BINDINGS = [
        # File operations
        Binding("ctrl+o", "open_file", "Open"),
        Binding("ctrl+s", "save_file", "Save"),
        Binding("f2", "save_as_file", "Save As"),
        Binding("ctrl+n", "new_file", "New"),
        Binding("ctrl+q", "quit", "Quit"),
        
        # Edit operations
        Binding("ctrl+z", "undo", "Undo"),
        Binding("ctrl+y", "redo", "Redo"),
        Binding("ctrl+x", "cut", "Cut"),
        Binding("ctrl+c", "copy", "Copy"),
        Binding("ctrl+v", "paste", "Paste"),
        
        # Find/Replace
        Binding("ctrl+f", "find", "Find"),
        Binding("ctrl+r", "replace", "Replace"),
        Binding("ctrl+g", "goto_line", "Go to Line"),
        
        # Mode toggle
        Binding("insert", "toggle_insert_mode", "Insert/Replace"),
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buffer = TextBuffer()
        self.scroll_offset_row = 0
        self.scroll_offset_col = 0
        self.clipboard_text = ""
        
    def compose(self) -> ComposeResult:
        """Create the text editor layout"""
        with Horizontal():
            with Vertical(id="editor-container"):
                yield TextArea("", id="text-area", show_line_numbers=config.show_line_numbers)
    
    def on_mount(self) -> None:
        """Called when widget is mounted"""
        self._update_text_area()
        
    def _update_text_area(self) -> None:
        """Update the text area with current buffer content"""
        text_area = self.query_one("#text-area", TextArea)
        content = '\n'.join(self.buffer.lines)
        text_area.text = content
        
        # Set cursor position
        cursor_row, cursor_col = self.buffer.get_cursor_position()
        try:
            text_area.cursor_location = (cursor_row, cursor_col)
        except:
            pass  # Ignore cursor positioning errors
        
        # Post update message
        self.post_message(EditorUpdate())
    
    def _sync_from_text_area(self) -> None:
        """Sync buffer from text area content"""
        text_area = self.query_one("#text-area", TextArea)
        content = text_area.text
        
        # Update buffer lines
        self.buffer.lines = content.splitlines() or [""]
        
        # Update cursor position
        if hasattr(text_area, 'cursor_location'):
            row, col = text_area.cursor_location
            self.buffer.set_cursor_position(row, col)
        
        self.buffer.modified = True
        
    def load_file(self, file_path: Path, encoding: Optional[str] = None) -> None:
        """Load a file into the editor"""
        try:
            self.buffer.load_file(file_path, encoding)
            self._update_text_area()
        except Exception as e:
            # Handle file loading errors
            self.app.notify(f"Error loading file: {e}", severity="error")
    
    def save_file(self, file_path: Optional[Path] = None) -> bool:
        """Save the current buffer to a file"""
        try:
            self._sync_from_text_area()
            self.buffer.save_file(file_path)
            self._update_text_area()  # Refresh to clear modified flag
            return True
        except Exception as e:
            self.app.notify(f"Error saving file: {e}", severity="error")
            return False
    
    def new_file(self, file_path: Optional[Path] = None) -> None:
        """Create a new file"""
        self.buffer = TextBuffer()
        if file_path:
            self.buffer.file_path = file_path
        self._update_text_area()
    
    # Action handlers
    def action_open_file(self) -> None:
        """Open file action"""
        # In a full implementation, this would show a file dialog
        self.app.notify("Open file functionality not yet implemented")
    
    def action_save_file(self) -> None:
        """Save file action"""
        if self.buffer.file_path:
            # Save to current file immediately
            if self.save_file():
                self.app.notify(f"Saved: {self.buffer.file_path.name}", severity="success")
            else:
                self.app.notify("Save failed", severity="error")
        else:
            # No file path - trigger save as
            self.action_save_as_file()
    
    def action_save_as_file(self) -> None:
        """Save As file action"""
        # In a full implementation, this would show a save dialog
        self.app.notify("Save As functionality not yet implemented")
    
    def action_new_file(self) -> None:
        """New file action"""
        self.new_file()
    
    def action_quit(self) -> None:
        """Quit application action"""
        if self.buffer.modified:
            # In a full implementation, show save confirmation dialog
            pass
        self.app.exit()
    
    def action_undo(self) -> None:
        """Undo action"""
        if self.buffer.undo():
            self._update_text_area()
        else:
            self.app.notify("Nothing to undo")
    
    def action_redo(self) -> None:
        """Redo action"""
        if self.buffer.redo():
            self._update_text_area()
        else:
            self.app.notify("Nothing to redo")
    
    def action_cut(self) -> None:
        """Cut action"""
        text_area = self.query_one("#text-area", TextArea)
        if text_area.selected_text:
            self.clipboard_text = text_area.selected_text
            text_area.delete_selection()
            self._sync_from_text_area()
            self._update_text_area()
    
    def action_copy(self) -> None:
        """Copy action"""
        text_area = self.query_one("#text-area", TextArea)
        if text_area.selected_text:
            self.clipboard_text = text_area.selected_text
    
    def action_paste(self) -> None:
        """Paste action"""
        if self.clipboard_text:
            text_area = self.query_one("#text-area", TextArea)
            text_area.insert(self.clipboard_text)
            self._sync_from_text_area()
            self._update_text_area()
    
    def action_find(self) -> None:
        """Find action"""
        from .dialogs import FindReplaceDialog
        self.app.push_screen(FindReplaceDialog())
    
    def action_replace(self) -> None:
        """Replace action"""
        from .dialogs import FindReplaceDialog
        self.app.push_screen(FindReplaceDialog())
    
    def action_goto_line(self) -> None:
        """Go to line action"""
        from .dialogs import GoToLineDialog
        max_lines = self.buffer.get_line_count()
        self.app.push_screen(GoToLineDialog(max_lines))
    
    def action_toggle_insert_mode(self) -> None:
        """Toggle insert/replace mode"""
        config.insert_mode = not config.insert_mode
        mode = "Insert" if config.insert_mode else "Replace"
        self.app.notify(f"Mode: {mode}")
    
    def get_cursor_position(self) -> tuple[int, int]:
        """Get current cursor position"""
        return self.buffer.get_cursor_position()
    
    def get_file_path(self) -> Optional[Path]:
        """Get current file path"""
        return self.buffer.file_path
    
    def is_modified(self) -> bool:
        """Check if buffer is modified"""
        return self.buffer.modified
    
    def get_encoding(self) -> str:
        """Get current file encoding"""
        return self.buffer.encoding
