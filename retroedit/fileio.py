"""
File I/O operations for RetroEdit
Handles file loading/saving with encoding detection and conversion
"""

import chardet
from pathlib import Path
from typing import Tuple, Optional
from .config import config


def detect_encoding(file_path: Path) -> str:
    """
    Detect the encoding of a file using chardet
    Returns the detected encoding or 'utf-8' as fallback
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        
        if not raw_data:
            return 'utf-8'
        
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        
        if encoding and result['confidence'] > 0.7:
            return encoding.lower()
        else:
            return 'utf-8'
    except Exception:
        return 'utf-8'


def load_file(file_path: Path, encoding: Optional[str] = None) -> Tuple[str, str]:
    """
    Load a file with specified or detected encoding
    Returns tuple of (content, encoding_used)
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Use provided encoding or detect it
    if encoding is None:
        encoding = detect_encoding(file_path)
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        return content, encoding
    except UnicodeDecodeError:
        # Fallback to utf-8 if specified encoding fails
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content, 'utf-8'
        except UnicodeDecodeError:
            # Last resort: latin-1 (can decode any byte sequence)
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
            return content, 'latin-1'


def save_file(file_path: Path, content: str, encoding: Optional[str] = None) -> None:
    """
    Save content to a file with specified encoding
    Uses config encoding if not specified
    """
    if encoding is None:
        encoding = config.encoding
    
    # Ensure parent directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert line endings according to config
    line_ending = config.get_line_ending_chars()
    
    # Normalize line endings first (convert all to \n)
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Apply desired line ending
    if line_ending != '\n':
        content = content.replace('\n', line_ending)
    
    try:
        with open(file_path, 'w', encoding=encoding, newline='') as f:
            f.write(content)
    except UnicodeEncodeError as e:
        raise ValueError(f"Cannot encode file with {encoding}: {e}")


def get_file_info(file_path: Path) -> dict:
    """
    Get information about a file (size, modification time, etc.)
    """
    if not file_path.exists():
        return {
            'exists': False,
            'size': 0,
            'modified': None,
            'readable': False,
            'writable': False
        }
    
    stat = file_path.stat()
    
    return {
        'exists': True,
        'size': stat.st_size,
        'modified': stat.st_mtime,
        'readable': file_path.is_file() and file_path.stat().st_mode & 0o444,
        'writable': file_path.is_file() and file_path.stat().st_mode & 0o200
    }


def backup_file(file_path: Path) -> Path:
    """
    Create a backup of the file before saving
    Returns the path to the backup file
    """
    backup_path = file_path.with_suffix(file_path.suffix + '.bak')
    
    if file_path.exists():
        import shutil
        shutil.copy2(file_path, backup_path)
    
    return backup_path
