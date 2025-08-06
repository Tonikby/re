"""
Dialog widgets for RetroEdit
Implements Save As, Find/Replace, and Go to Line dialogs
"""

from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Checkbox
from textual.message import Message
from pathlib import Path
from typing import Optional


class DialogResult(Message):
    """Base message for dialog results"""
    
    def __init__(self, result: Optional[dict] = None, **kwargs):
        super().__init__(**kwargs)
        self.result = result


class SaveAsDialog(ModalScreen):
    """Save As dialog"""
    
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("enter", "save", "Save"),
    ]
    
    def __init__(self, current_path: Optional[Path] = None, **kwargs):
        super().__init__(**kwargs)
        self.current_path = current_path
    
    def compose(self) -> ComposeResult:
        with Grid(id="save-as-dialog"):
            yield Label("Save As", id="dialog-title")
            yield Label("File name:")
            yield Input(
                value=str(self.current_path) if self.current_path else "",
                placeholder="Enter file path...",
                id="file-input"
            )
            with Horizontal():
                yield Button("Save", variant="primary", id="save-button")
                yield Button("Cancel", variant="default", id="cancel-button")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-button":
            self.action_save()
        elif event.button.id == "cancel-button":
            self.action_cancel()
    
    def action_save(self) -> None:
        """Save with entered filename"""
        input_widget = self.query_one("#file-input", Input)
        file_path = input_widget.value.strip()
        
        if file_path:
            self.post_message(DialogResult({"action": "save", "path": Path(file_path)}))
            self.app.pop_screen()
        else:
            input_widget.focus()
    
    def action_cancel(self) -> None:
        """Cancel dialog"""
        self.post_message(DialogResult({"action": "cancel"}))
        self.app.pop_screen()


class FindReplaceDialog(ModalScreen):
    """Find and Replace dialog"""
    
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("enter", "find_next", "Find Next"),
        ("f3", "find_next", "Find Next"),
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_search = ""
        self.last_replace = ""
    
    def compose(self) -> ComposeResult:
        with Grid(id="find-replace-dialog"):
            yield Label("Find and Replace", id="dialog-title")
            
            yield Label("Find:")
            yield Input(placeholder="Text to find...", id="find-input")
            
            yield Label("Replace:")
            yield Input(placeholder="Replace with...", id="replace-input")
            
            yield Checkbox("Match case", id="case-checkbox")
            
            with Horizontal():
                yield Button("Find Next", variant="primary", id="find-button")
                yield Button("Replace", variant="default", id="replace-button")
                yield Button("Replace All", variant="default", id="replace-all-button")
                yield Button("Close", variant="default", id="close-button")
    
    def on_mount(self) -> None:
        """Focus find input when dialog opens"""
        self.query_one("#find-input", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "find-button":
            self.action_find_next()
        elif event.button.id == "replace-button":
            self.action_replace()
        elif event.button.id == "replace-all-button":
            self.action_replace_all()
        elif event.button.id == "close-button":
            self.action_cancel()
    
    def action_find_next(self) -> None:
        """Find next occurrence"""
        find_input = self.query_one("#find-input", Input)
        case_checkbox = self.query_one("#case-checkbox", Checkbox)
        
        find_text = find_input.value.strip()
        if find_text:
            self.last_search = find_text
            self.post_message(DialogResult({
                "action": "find",
                "text": find_text,
                "case_sensitive": case_checkbox.value
            }))
    
    def action_replace(self) -> None:
        """Replace current occurrence"""
        find_input = self.query_one("#find-input", Input)
        replace_input = self.query_one("#replace-input", Input)
        case_checkbox = self.query_one("#case-checkbox", Checkbox)
        
        find_text = find_input.value.strip()
        replace_text = replace_input.value
        
        if find_text:
            self.last_search = find_text
            self.last_replace = replace_text
            self.post_message(DialogResult({
                "action": "replace",
                "find_text": find_text,
                "replace_text": replace_text,
                "case_sensitive": case_checkbox.value
            }))
    
    def action_replace_all(self) -> None:
        """Replace all occurrences"""
        find_input = self.query_one("#find-input", Input)
        replace_input = self.query_one("#replace-input", Input)
        case_checkbox = self.query_one("#case-checkbox", Checkbox)
        
        find_text = find_input.value.strip()
        replace_text = replace_input.value
        
        if find_text:
            self.last_search = find_text
            self.last_replace = replace_text
            self.post_message(DialogResult({
                "action": "replace_all",
                "find_text": find_text,
                "replace_text": replace_text,
                "case_sensitive": case_checkbox.value
            }))
    
    def action_cancel(self) -> None:
        """Close dialog"""
        self.app.pop_screen()


class GoToLineDialog(ModalScreen):
    """Go to Line dialog"""
    
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("enter", "go_to_line", "Go"),
    ]
    
    def __init__(self, max_lines: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.max_lines = max_lines
    
    def compose(self) -> ComposeResult:
        with Grid(id="goto-dialog"):
            yield Label("Go to Line", id="dialog-title")
            yield Label(f"Line number (1-{self.max_lines}):")
            yield Input(
                placeholder=f"1-{self.max_lines}",
                id="line-input",
                type="integer"
            )
            with Horizontal():
                yield Button("Go", variant="primary", id="go-button")
                yield Button("Cancel", variant="default", id="cancel-button")
    
    def on_mount(self) -> None:
        """Focus line input when dialog opens"""
        self.query_one("#line-input", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go-button":
            self.action_go_to_line()
        elif event.button.id == "cancel-button":
            self.action_cancel()
    
    def action_go_to_line(self) -> None:
        """Go to specified line"""
        input_widget = self.query_one("#line-input", Input)
        
        try:
            line_num = int(input_widget.value)
            if 1 <= line_num <= self.max_lines:
                self.post_message(DialogResult({
                    "action": "goto",
                    "line": line_num - 1  # Convert to 0-based
                }))
                self.app.pop_screen()
            else:
                # Invalid line number
                input_widget.focus()
                # Could add error message here
        except ValueError:
            # Invalid input
            input_widget.focus()
    
    def action_cancel(self) -> None:
        """Cancel dialog"""
        self.post_message(DialogResult({"action": "cancel"}))
        self.app.pop_screen()


class OpenFileDialog(ModalScreen):
    """Simple open file dialog"""
    
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("enter", "open", "Open"),
    ]
    
    def compose(self) -> ComposeResult:
        with Grid(id="open-file-dialog"):
            yield Label("Open File", id="dialog-title")
            yield Label("File path:")
            yield Input(
                placeholder="Enter file path...",
                id="file-input"
            )
            with Horizontal():
                yield Button("Open", variant="primary", id="open-button")
                yield Button("Cancel", variant="default", id="cancel-button")
    
    def on_mount(self) -> None:
        """Focus file input when dialog opens"""
        self.query_one("#file-input", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "open-button":
            self.action_open()
        elif event.button.id == "cancel-button":
            self.action_cancel()
    
    def action_open(self) -> None:
        """Open specified file"""
        input_widget = self.query_one("#file-input", Input)
        file_path = input_widget.value.strip()
        
        if file_path:
            self.post_message(DialogResult({"action": "open", "path": Path(file_path)}))
            self.app.pop_screen()
        else:
            input_widget.focus()
    
    def action_cancel(self) -> None:
        """Cancel dialog"""
        self.post_message(DialogResult({"action": "cancel"}))
        self.app.pop_screen()
