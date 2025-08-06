"""
Main RetroEdit application
Textual-based retro text editor inspired by MS-DOS Edit
"""

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.binding import Binding
from textual.widgets import Footer
from textual.screen import Screen
from pathlib import Path
from typing import Optional
import os
import sys

from .ui.menu import MenuBar, MenuAction
from .ui.status import StatusBar
from .ui.text_editor import TextEditor, EditorUpdate
from .config import config


def get_css_path() -> str:
    """Get the path to the CSS file, handling both development and packaged versions"""
    # Check if we're running in a PyInstaller bundle
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller bundle - look in the temporary directory
        css_path = Path(sys._MEIPASS) / "retroedit.tcss"
        if css_path.exists():
            return str(css_path)
        
        # Fallback: look in the retroedit subdirectory
        css_path = Path(sys._MEIPASS) / "retroedit" / "retroedit.tcss"
        if css_path.exists():
            return str(css_path)
    
    # Development mode - look relative to this file
    module_dir = Path(__file__).parent
    css_path = module_dir.parent / "retroedit.tcss"
    if css_path.exists():
        return str(css_path)
    
    # Look in the same directory as this module
    css_path = module_dir / "retroedit.tcss"
    if css_path.exists():
        return str(css_path)
    
    # Fallback to default name (will use Textual's default styling)
    return ""


class RetroEditScreen(Screen):
    """Main screen for RetroEdit"""
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("f1", "show_help", "Help"),
        Binding("f10", "toggle_menu", "Menu"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create the main layout"""
        yield MenuBar(id="menu-bar")
        yield TextEditor(id="text-editor")
        if config.show_status_bar:
            yield StatusBar(id="status-bar")
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when screen is mounted"""
        self.title = "RetroEdit - Untitled"
        self._update_status_bar()
    
    def on_menu_action(self, message: MenuAction) -> None:
        """Handle menu actions"""
        action = message.action
        
        if action == "file_new":
            self.action_new_file()
        elif action == "file_open":
            self.action_open_file()
        elif action == "file_save":
            self.action_save_file()
        elif action == "file_save_as":
            self.action_save_as_file()
        elif action == "file_exit":
            self.action_quit()
        elif action == "edit_undo":
            self._get_editor().action_undo()
        elif action == "edit_redo":
            self._get_editor().action_redo()
        elif action == "edit_cut":
            self._get_editor().action_cut()
        elif action == "edit_copy":
            self._get_editor().action_copy()
        elif action == "edit_paste":
            self._get_editor().action_paste()
        elif action == "edit_find":
            self._get_editor().action_find()
        elif action == "edit_replace":
            self._get_editor().action_replace()
        elif action == "edit_goto":
            self._get_editor().action_goto_line()
        elif action == "view_status_bar":
            self.action_toggle_status_bar()
        elif action == "view_line_numbers":
            self.action_toggle_line_numbers()
        elif action.startswith("view_line_ending_"):
            ending = action.split("_")[-1].upper()
            self.action_set_line_ending(ending)
        elif action.startswith("view_encoding_"):
            encoding = action.split("_")[-1].replace("utf8", "utf-8")
            self.action_set_encoding(encoding)
        elif action == "help_about":
            self.action_show_about()
        elif action == "help_shortcuts":
            self.action_show_shortcuts()
    
    def on_editor_update(self, message: EditorUpdate) -> None:
        """Handle editor updates"""
        self._update_status_bar()
        self._update_title()
    
    def _get_editor(self) -> TextEditor:
        """Get the text editor widget"""
        return self.query_one("#text-editor", TextEditor)
    
    def _get_status_bar(self) -> Optional[StatusBar]:
        """Get the status bar widget if visible"""
        try:
            return self.query_one("#status-bar", StatusBar)
        except:
            return None
    
    def _update_status_bar(self) -> None:
        """Update the status bar with current editor state"""
        status_bar = self._get_status_bar()
        if not status_bar:
            return
        
        editor = self._get_editor()
        cursor_row, cursor_col = editor.get_cursor_position()
        
        status_bar.update_status(
            file_path=editor.get_file_path(),
            cursor_row=cursor_row,
            cursor_col=cursor_col,
            modified=editor.is_modified(),
            encoding=editor.get_encoding()
        )
    
    def _update_title(self) -> None:
        """Update the window title"""
        editor = self._get_editor()
        file_path = editor.get_file_path()
        modified = editor.is_modified()
        
        if file_path:
            filename = file_path.name
        else:
            filename = "Untitled"
        
        title = f"RetroEdit - {filename}"
        if modified:
            title += " *"
        
        self.title = title
    
    # Action handlers
    def action_quit(self) -> None:
        """Quit the application"""
        editor = self._get_editor()
        if editor.is_modified():
            # In a full implementation, show save confirmation dialog
            pass
        self.app.exit()
    
    def action_new_file(self) -> None:
        """Create a new file"""
        self._get_editor().new_file()
        self._update_status_bar()
        self._update_title()
    
    def action_open_file(self) -> None:
        """Open a file"""
        # In a full implementation, show file dialog
        self.app.notify("Open file functionality not yet fully implemented")
    
    def action_save_file(self) -> None:
        """Save current file"""
        editor = self._get_editor()
        if editor.get_file_path():
            if editor.save_file():
                self.app.notify("File saved")
                self._update_status_bar()
                self._update_title()
        else:
            self.action_save_as_file()
    
    def action_save_as_file(self) -> None:
        """Save file with new name"""
        # In a full implementation, show save dialog
        self.app.notify("Save As functionality not yet fully implemented")
    
    def action_toggle_status_bar(self) -> None:
        """Toggle status bar visibility"""
        config.show_status_bar = not config.show_status_bar
        # In a full implementation, would need to recreate the layout
        self.app.notify(f"Status bar: {'On' if config.show_status_bar else 'Off'}")
    
    def action_toggle_line_numbers(self) -> None:
        """Toggle line numbers visibility"""
        config.show_line_numbers = not config.show_line_numbers
        # In a full implementation, would need to update text area
        self.app.notify(f"Line numbers: {'On' if config.show_line_numbers else 'Off'}")
    
    def action_set_line_ending(self, ending: str) -> None:
        """Set line ending format"""
        config.line_ending = ending
        self._update_status_bar()
        self.app.notify(f"Line endings: {ending}")
    
    def action_set_encoding(self, encoding: str) -> None:
        """Set text encoding"""
        config.encoding = encoding
        self._update_status_bar()
        self.app.notify(f"Encoding: {encoding}")
    
    def action_show_help(self) -> None:
        """Show help dialog"""
        self.app.notify("Help functionality not yet implemented")
    
    def action_show_about(self) -> None:
        """Show about dialog"""
        self.app.notify("RetroEdit v1.0.0 - A retro text editor inspired by MS-DOS Edit")
    
    def action_show_shortcuts(self) -> None:
        """Show keyboard shortcuts"""
        shortcuts = [
            "Ctrl+N - New file",
            "Ctrl+O - Open file", 
            "Ctrl+S - Save file",
            "F2 - Save As",
            "Ctrl+Q - Quit",
            "Ctrl+Z - Undo",
            "Ctrl+Y - Redo",
            "Ctrl+X - Cut",
            "Ctrl+C - Copy",
            "Ctrl+V - Paste",
            "Ctrl+F - Find",
            "Ctrl+R - Replace",
            "Ctrl+G - Go to Line",
            "Insert - Toggle Insert/Replace mode",
            "F1 - Help",
            "F10 - Menu"
        ]
        self.app.notify("Keyboard Shortcuts:\n" + "\n".join(shortcuts))
    
    def action_toggle_menu(self) -> None:
        """Toggle menu bar focus"""
        menu_bar = self.query_one("#menu-bar", MenuBar)
        menu_bar.action_toggle_menu()


class RetroEditApp(App):
    """Main RetroEdit application"""
    
    TITLE = "RetroEdit"
    
    def __init__(self, **kwargs):
        # Set CSS path dynamically
        css_path = get_css_path()
        if css_path:
            self.CSS_PATH = css_path
        super().__init__(**kwargs)
        self.file_to_open: Optional[Path] = None
        self.encoding: str = "utf-8"
    
    def on_mount(self) -> None:
        """Called when app is mounted"""
        self.push_screen(RetroEditScreen())
        
        # Open file if specified
        if self.file_to_open:
            screen = self.screen
            if isinstance(screen, RetroEditScreen):
                editor = screen._get_editor()
                try:
                    editor.load_file(self.file_to_open, self.encoding)
                    screen._update_status_bar()
                    screen._update_title()
                except Exception as e:
                    self.notify(f"Error loading file: {e}", severity="error")
    
    def open_file(self, file_path: Path, encoding: str = "utf-8") -> None:
        """Set file to open on startup"""
        self.file_to_open = file_path
        self.encoding = encoding
    
    def new_file(self, file_path: Path) -> None:
        """Set up for new file"""
        self.file_to_open = file_path
