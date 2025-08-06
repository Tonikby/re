#!/usr/bin/env python3
"""
Release preparation script for RetroEdit
Checks project status and prepares for release
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command and return the result"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"STDERR: {result.stderr}")
        sys.exit(1)
    return result


def check_git_status():
    """Check if git repository is clean"""
    print("🔍 Checking Git status...")
    result = run_command("git status --porcelain")
    if result.stdout.strip():
        print("⚠️  Warning: Working directory is not clean")
        print(result.stdout)
    else:
        print("✅ Working directory is clean")


def check_tests():
    """Run tests to ensure everything works"""
    print("\n🧪 Running tests...")
    try:
        result = run_command("source venv/bin/activate && python -m pytest tests/ -v", check=False)
        if result.returncode == 0:
            print("✅ All tests passed")
        else:
            print("❌ Tests failed")
            return False
    except:
        print("⚠️  pytest not available, running basic import test...")
        result = run_command("source venv/bin/activate && python -c 'from retroedit.app import RetroEditApp; print(\"Import successful\")'")
        print("✅ Basic import test passed")
    
    return True


def check_demo():
    """Run demo script"""
    print("\n🎮 Running demo script...")
    result = run_command("source venv/bin/activate && python demo.py", check=False)
    if result.returncode == 0:
        print("✅ Demo script runs successfully")
        return True
    else:
        print("❌ Demo script failed")
        print(result.stderr)
        return False


def check_build():
    """Test build process"""
    print("\n🔨 Testing build process...")
    try:
        result = run_command("source venv/bin/activate && python -c 'import PyInstaller; print(\"PyInstaller available\")'", check=False)
        if result.returncode == 0:
            print("✅ PyInstaller is available for building")
            return True
        else:
            print("⚠️  PyInstaller not available - install with: pip install pyinstaller")
            return False
    except:
        print("⚠️  Could not check PyInstaller availability")
        return False


def check_files():
    """Check that all required files exist"""
    print("\n📁 Checking required files...")
    
    required_files = [
        "README.md",
        "LICENSE", 
        "requirements.txt",
        "setup.py",
        "main.py",
        "retroedit/__init__.py",
        "retroedit/app.py",
        "retroedit/main.py",
        ".gitignore",
        "CHANGELOG.md",
        "CONTRIBUTING.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True


def show_version_info():
    """Show version information"""
    print("\n📋 Version Information:")
    
    # Get version from __init__.py
    init_file = Path("retroedit/__init__.py")
    if init_file.exists():
        content = init_file.read_text()
        for line in content.splitlines():
            if line.startswith('__version__'):
                print(f"  Package version: {line.split('=')[1].strip().strip('\"')}")
                break
    
    # Get current git branch and commit
    try:
        branch = run_command("git branch --show-current").stdout.strip()
        commit = run_command("git rev-parse --short HEAD").stdout.strip()
        print(f"  Git branch: {branch}")
        print(f"  Git commit: {commit}")
    except:
        print("  Git info: Not available")


def show_summary():
    """Show release readiness summary"""
    print("\n" + "="*50)
    print("🚀 RELEASE READINESS SUMMARY")
    print("="*50)
    
    checks = [
        ("Files", check_files()),
        ("Tests", check_tests()),
        ("Demo", check_demo()),
        ("Build Tools", check_build()),
    ]
    
    all_passed = all(result for _, result in checks)
    
    for name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name:<12} {status}")
    
    print("\n" + "="*50)
    
    if all_passed:
        print("🎉 PROJECT IS READY FOR RELEASE!")
        print("\nNext steps:")
        print("1. git add -A")
        print("2. git commit -m 'Release v1.0.0'")
        print("3. git tag v1.0.0")
        print("4. git push origin main --tags")
    else:
        print("⚠️  PROJECT NEEDS ATTENTION BEFORE RELEASE")
        print("\nPlease fix the failing checks above.")
    
    print("="*50)


def main():
    """Main release check process"""
    print("RetroEdit Release Preparation")
    print("=" * 50)
    
    check_git_status()
    show_version_info()
    show_summary()


if __name__ == "__main__":
    main()
