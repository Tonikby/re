#!/usr/bin/env python3
"""
RetroEdit - A retro-style text editor inspired by MS-DOS Edit
Main entry point for the application
"""

import sys
import argparse
from pathlib import Path
from retroedit.app import RetroEditApp


def main():
    """Main entry point for RetroEdit"""
    parser = argparse.ArgumentParser(
        description="RetroEdit - A retro-style text editor"
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
