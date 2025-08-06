"""
Configuration management for RetroEdit
Handles view options, encoding, tab settings, and other preferences
"""

from dataclasses import dataclass
from typing import Literal
import json
from pathlib import Path


LineEnding = Literal["CR", "LF", "CRLF"]
Encoding = Literal["utf-8", "cp437", "cp1252", "latin-1"]


@dataclass
class RetroEditConfig:
    """Configuration settings for RetroEdit"""
    
    # View settings
    show_line_numbers: bool = True
    show_status_bar: bool = True
    show_scrollbar: bool = True
    
    # Text settings
    tab_size: int = 4
    use_spaces: bool = True
    line_ending: LineEnding = "CRLF"
    encoding: Encoding = "utf-8"
    
    # Editor settings
    insert_mode: bool = True
    wrap_lines: bool = False
    
    # Theme settings
    retro_colors: bool = True
    black_background: bool = True  # True = black theme (default), False = blue theme
    
    def save_to_file(self, path: Path) -> None:
        """Save configuration to a JSON file"""
        config_dict = {
            "show_line_numbers": self.show_line_numbers,
            "show_status_bar": self.show_status_bar,
            "show_scrollbar": self.show_scrollbar,
            "tab_size": self.tab_size,
            "use_spaces": self.use_spaces,
            "line_ending": self.line_ending,
            "encoding": self.encoding,
            "insert_mode": self.insert_mode,
            "wrap_lines": self.wrap_lines,
            "retro_colors": self.retro_colors,
            "black_background": self.black_background,
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2)
    
    @classmethod
    def load_from_file(cls, path: Path) -> 'RetroEditConfig':
        """Load configuration from a JSON file"""
        if not path.exists():
            return cls()
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            
            return cls(
                show_line_numbers=config_dict.get("show_line_numbers", True),
                show_status_bar=config_dict.get("show_status_bar", True),
                show_scrollbar=config_dict.get("show_scrollbar", True),
                tab_size=config_dict.get("tab_size", 4),
                use_spaces=config_dict.get("use_spaces", True),
                line_ending=config_dict.get("line_ending", "CRLF"),
                encoding=config_dict.get("encoding", "utf-8"),
                insert_mode=config_dict.get("insert_mode", True),
                wrap_lines=config_dict.get("wrap_lines", False),
                retro_colors=config_dict.get("retro_colors", True),
                black_background=config_dict.get("black_background", True),
            )
        except (json.JSONDecodeError, KeyError):
            # Return default config if file is corrupted
            return cls()
    
    def get_line_ending_chars(self) -> str:
        """Get the actual line ending characters"""
        endings = {
            "CR": "\r",
            "LF": "\n", 
            "CRLF": "\r\n"
        }
        return endings[self.line_ending]


# Global config instance
config = RetroEditConfig()
