#!/usr/bin/env python3
"""
Build script for RetroEdit
Creates standalone executables for Windows and macOS
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if build dependencies are available"""
    try:
        import PyInstaller
        print("✓ PyInstaller found")
        return True
    except ImportError:
        print("✗ PyInstaller not found. Install with: pip install pyinstaller")
        return False


def build_with_pyinstaller():
    """Build using PyInstaller"""
    print("Building with PyInstaller...")
    
    # Clean previous builds
    if Path("dist").exists():
        shutil.rmtree("dist")
    if Path("build").exists():
        shutil.rmtree("build")
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "retroedit",
        "--add-data", "retroedit.tcss:.",
        "--hidden-import", "retroedit",
        "--hidden-import", "retroedit.ui",
        "main.py"
    ]
    
    # Add platform-specific options
    if sys.platform == "win32":
        cmd.extend(["--icon", "icon.ico"])
    elif sys.platform == "darwin":
        cmd.extend(["--icon", "icon.icns"])
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Build successful!")
        
        # Show output location
        dist_path = Path("dist")
        if dist_path.exists():
            executables = list(dist_path.glob("*"))
            if executables:
                print(f"Executable created: {executables[0]}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def build_with_nuitka():
    """Build using Nuitka (alternative)"""
    try:
        import nuitka
    except ImportError:
        print("Nuitka not available. Install with: pip install nuitka")
        return False
    
    print("Building with Nuitka...")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--onefile",
        "--console",
        "--output-filename=retroedit",
        "main.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✓ Nuitka build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Nuitka build failed: {e}")
        return False


def create_package():
    """Create a distributable package"""
    print("Creating package...")
    
    # Create package directory
    package_dir = Path("package")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy executable
    dist_path = Path("dist")
    if dist_path.exists():
        for exe in dist_path.glob("*"):
            if exe.is_file():
                shutil.copy2(exe, package_dir)
                print(f"✓ Copied {exe.name}")
    
    # Copy documentation
    docs = ["README.md", "re_Technical_Requirements.md"]
    for doc in docs:
        doc_path = Path(doc)
        if doc_path.exists():
            shutil.copy2(doc_path, package_dir)
            print(f"✓ Copied {doc}")
    
    # Create sample config
    sample_config = package_dir / "sample_config.json"
    sample_config.write_text('''{
  "show_line_numbers": true,
  "show_status_bar": true,
  "show_scrollbar": true,
  "tab_size": 4,
  "use_spaces": true,
  "line_ending": "CRLF",
  "encoding": "utf-8",
  "insert_mode": true,
  "wrap_lines": false,
  "retro_colors": true
}''')
    print("✓ Created sample configuration")
    
    print(f"Package created in: {package_dir}")


def main():
    """Main build process"""
    print("RetroEdit Build Script")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    print(f"Building for platform: {sys.platform}")
    
    # Build with PyInstaller
    if build_with_pyinstaller():
        create_package()
        print("\n✓ Build complete!")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
