"""
Menu bar component for RetroEdit
Provides File, Edit, View, and Help menus with keyboard navigation
"""

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Button, Label
from textual.containers import Horizontal
from textual.message import Message
from textual.binding import Binding
from typing import Dict, List, Callable, Optional


class MenuAction(Message):
    """Message sent when a menu action is selected"""
    
    def __init__(self, action: str, **kwargs):
        super().__init__(**kwargs)
        self.action = action


class MenuBar(Widget):
    """Menu bar widget with File, Edit, View, Help menus"""
    
    BINDINGS = [
        Binding("f10", "toggle_menu", "Menu"),
        Binding("alt+f", "show_file_menu", "File"),
        Binding("alt+e", "show_edit_menu", "Edit"),  
        Binding("alt+v", "show_view_menu", "View"),
        Binding("alt+h", "show_help_menu", "Help"),
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_menu: Optional[str] = None
        self.menu_items = self._build_menu_structure()
    
    def compose(self) -> ComposeResult:
        """Create the menu bar layout"""
        with Horizontal(id="menu-container"):
            yield Button("File", id="file-menu", variant="primary")
            yield Button("Edit", id="edit-menu", variant="primary") 
            yield Button("View", id="view-menu", variant="primary")
            yield Button("Help", id="help-menu", variant="primary")
            yield Label("", id="menu-spacer")
    
    def _build_menu_structure(self) -> Dict[str, List[Dict]]:
        """Build the menu structure"""
        return {
            "file": [
                {"label": "New", "action": "file_new", "key": "Ctrl+N"},
                {"label": "Open...", "action": "file_open", "key": "Ctrl+O"},
                {"separator": True},
                {"label": "Save", "action": "file_save", "key": "Ctrl+S"},
                {"label": "Save As...", "action": "file_save_as", "key": "F2"},
                {"separator": True},
                {"label": "Exit", "action": "file_exit", "key": "Ctrl+Q"},
            ],
            "edit": [
                {"label": "Undo", "action": "edit_undo", "key": "Ctrl+Z"},
                {"label": "Redo", "action": "edit_redo", "key": "Ctrl+Y"},
                {"separator": True},
                {"label": "Cut", "action": "edit_cut", "key": "Ctrl+X"},
                {"label": "Copy", "action": "edit_copy", "key": "Ctrl+C"},
                {"label": "Paste", "action": "edit_paste", "key": "Ctrl+V"},
                {"separator": True},
                {"label": "Find", "action": "edit_find", "key": "Ctrl+F"},
                {"label": "Replace", "action": "edit_replace", "key": "Ctrl+R"},
                {"label": "Go to Line", "action": "edit_goto", "key": "Ctrl+G"},
            ],
            "view": [
                {"label": "Status Bar", "action": "view_status_bar", "checkable": True},
                {"label": "Line Numbers", "action": "view_line_numbers", "checkable": True},
                {"separator": True},
                {"label": "Theme", "action": "view_theme", "submenu": [
                    {"label": "Black", "action": "view_theme_black"},
                    {"label": "Blue", "action": "view_theme_blue"},
                ]},
                {"separator": True},
                {"label": "Line Endings", "action": "view_line_endings", "submenu": [
                    {"label": "CR", "action": "view_line_ending_cr"},
                    {"label": "LF", "action": "view_line_ending_lf"}, 
                    {"label": "CRLF", "action": "view_line_ending_crlf"},
                ]},
                {"label": "Encoding", "action": "view_encoding", "submenu": [
                    {"label": "UTF-8", "action": "view_encoding_utf8"},
                    {"label": "CP437", "action": "view_encoding_cp437"},
                    {"label": "CP1252", "action": "view_encoding_cp1252"},
                    {"label": "Latin-1", "action": "view_encoding_latin1"},
                ]},
            ],
            "help": [
                {"label": "Keyboard Shortcuts", "action": "help_shortcuts"},
                {"separator": True},
                {"label": "About RetroEdit", "action": "help_about"},
            ],
        }
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle menu button press"""
        button_id = event.button.id
        
        if button_id == "file-menu":
            self.action_show_file_menu()
        elif button_id == "edit-menu":
            self.action_show_edit_menu()
        elif button_id == "view-menu":
            self.action_show_view_menu()
        elif button_id == "help-menu":
            self.action_show_help_menu()
    
    def action_toggle_menu(self) -> None:
        """Toggle menu bar activation"""
        if self.active_menu:
            self.active_menu = None
        else:
            self.action_show_file_menu()
    
    def action_show_file_menu(self) -> None:
        """Show File menu"""
        self.active_menu = "file"
        self._show_menu_popup("file")
    
    def action_show_edit_menu(self) -> None:
        """Show Edit menu"""  
        self.active_menu = "edit"
        self._show_menu_popup("edit")
    
    def action_show_view_menu(self) -> None:
        """Show View menu"""
        self.active_menu = "view"
        self._show_menu_popup("view")
    
    def action_show_help_menu(self) -> None:
        """Show Help menu"""
        self.active_menu = "help"
        self._show_menu_popup("help")
    
    def _show_menu_popup(self, menu_name: str) -> None:
        """Show a menu popup (simplified for now)"""
        # For now, just trigger the first menu item as a demo
        # In a full implementation, this would show an actual popup menu
        menu_items = self.menu_items.get(menu_name, [])
        if menu_items:
            # Find the first non-separator item
            for item in menu_items:
                if not item.get("separator"):
                    action = item.get("action")
                    if action:
                        self.post_message(MenuAction(action))
                    break
    
    def trigger_action(self, action: str) -> None:
        """Trigger a menu action"""
        self.post_message(MenuAction(action))
    
    def on_mount(self) -> None:
        """Called when widget is mounted"""
        pass
