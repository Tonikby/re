#!/usr/bin/env python3
"""
RetroEdit main module - Entry point for the package
"""

import sys
import argparse
from pathlib import Path
from .app import RetroEditApp


def main():
    """Main entry point for RetroEdit"""
    parser = argparse.ArgumentParser(
        description="RetroEdit - A retro-style text editor inspired by MS-DOS Edit",
        prog="retroedit"
    )
    parser.add_argument(
        "file", 
        nargs="?", 
        help="File to open (optional)"
    )
    parser.add_argument(
        "--encoding", 
        default="utf-8", 
        help="Text encoding (default: utf-8)"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="RetroEdit 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Initialize the application
    app = RetroEditApp()
    
    # Open file if specified
    if args.file:
        file_path = Path(args.file)
        if file_path.exists():
            app.open_file(file_path, encoding=args.encoding)
        else:
            app.new_file(file_path)
    
    # Run the application
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nRetroEdit terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
