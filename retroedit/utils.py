"""
Utility functions for RetroEdit
Helper functions for text operations, formatting, etc.
"""

import re
from typing import List, Tuple, Optional


def wrap_text(text: str, width: int) -> List[str]:
    """
    Wrap text to specified width, breaking at word boundaries when possible
    """
    if not text:
        return [""]
    
    lines = []
    for line in text.splitlines():
        if len(line) <= width:
            lines.append(line)
        else:
            # Break long lines at word boundaries
            words = line.split()
            current_line = ""
            
            for word in words:
                if len(current_line + " " + word) <= width:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
                else:
                    if current_line:
                        lines.append(current_line)
                        current_line = word
                    else:
                        # Word is longer than width, break it
                        while len(word) > width:
                            lines.append(word[:width])
                            word = word[width:]
                        current_line = word
            
            if current_line:
                lines.append(current_line)
    
    return lines


def expand_tabs(text: str, tab_size: int = 4) -> str:
    """
    Expand tabs to spaces
    """
    return text.expandtabs(tab_size)


def count_leading_whitespace(line: str) -> int:
    """
    Count leading whitespace characters in a line
    """
    count = 0
    for char in line:
        if char in ' \t':
            count += 1
        else:
            break
    return count


def get_indentation(line: str, tab_size: int = 4) -> str:
    """
    Get the indentation string from a line
    """
    indent = ""
    for char in line:
        if char == ' ':
            indent += ' '
        elif char == '\t':
            indent += ' ' * tab_size
        else:
            break
    return indent


def normalize_line_endings(text: str, ending: str = "\n") -> str:
    """
    Normalize line endings in text
    """
    # First, normalize all line endings to \n
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Then apply the desired ending
    if ending != '\n':
        text = text.replace('\n', ending)
    
    return text


def find_matching_bracket(text: str, pos: int) -> Optional[int]:
    """
    Find matching bracket for the bracket at given position
    Returns None if no matching bracket found
    """
    if pos >= len(text) or pos < 0:
        return None
    
    char = text[pos]
    
    # Define bracket pairs
    open_brackets = "([{"
    close_brackets = ")]}"
    pairs = {"(": ")", "[": "]", "{": "}"}
    reverse_pairs = {v: k for k, v in pairs.items()}
    
    if char in open_brackets:
        # Find closing bracket
        target = pairs[char]
        count = 1
        for i in range(pos + 1, len(text)):
            if text[i] == char:
                count += 1
            elif text[i] == target:
                count -= 1
                if count == 0:
                    return i
    elif char in close_brackets:
        # Find opening bracket
        target = reverse_pairs[char]
        count = 1
        for i in range(pos - 1, -1, -1):
            if text[i] == char:
                count += 1
            elif text[i] == target:
                count -= 1
                if count == 0:
                    return i
    
    return None


def is_word_char(char: str) -> bool:
    """
    Check if character is a word character (letter, digit, or underscore)
    """
    return char.isalnum() or char == '_'


def find_word_boundaries(text: str, pos: int) -> Tuple[int, int]:
    """
    Find word boundaries around the given position
    Returns (start, end) positions
    """
    if pos >= len(text) or pos < 0:
        return pos, pos
    
    # Find start of word
    start = pos
    while start > 0 and is_word_char(text[start - 1]):
        start -= 1
    
    # Find end of word
    end = pos
    while end < len(text) and is_word_char(text[end]):
        end += 1
    
    return start, end


def escape_regex(text: str) -> str:
    """
    Escape special regex characters in text for literal search
    """
    return re.escape(text)


def find_all_occurrences(text: str, search: str, case_sensitive: bool = True) -> List[Tuple[int, int]]:
    """
    Find all occurrences of search string in text
    Returns list of (start, end) positions
    """
    if not search:
        return []
    
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = escape_regex(search)
    
    matches = []
    for match in re.finditer(pattern, text, flags):
        matches.append((match.start(), match.end()))
    
    return matches


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"


def truncate_string(text: str, max_length: int, ellipsis: str = "...") -> str:
    """
    Truncate string to maximum length, adding ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(ellipsis)] + ellipsis


def center_text(text: str, width: int, fill_char: str = " ") -> str:
    """
    Center text within specified width
    """
    return text.center(width, fill_char)


def get_line_and_column_from_index(text: str, index: int) -> Tuple[int, int]:
    """
    Convert character index to line and column numbers (0-based)
    """
    if index < 0 or index > len(text):
        return 0, 0
    
    line = text[:index].count('\n')
    if line == 0:
        column = index
    else:
        last_newline = text.rfind('\n', 0, index)
        column = index - last_newline - 1
    
    return line, column


def get_index_from_line_and_column(text: str, line: int, column: int) -> int:
    """
    Convert line and column numbers to character index
    """
    lines = text.splitlines(keepends=True)
    
    if line < 0 or line >= len(lines):
        return len(text)
    
    index = sum(len(lines[i]) for i in range(line))
    
    if column >= 0:
        line_text = lines[line].rstrip('\n\r')
        index += min(column, len(line_text))
    
    return index
