#!/usr/bin/env python3
"""
Setup script for RetroEdit
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
README_PATH = Path(__file__).parent / "README.md"
long_description = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""

# Read requirements
REQUIREMENTS_PATH = Path(__file__).parent / "requirements.txt"
requirements = []
if REQUIREMENTS_PATH.exists():
    with open(REQUIREMENTS_PATH, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f.readlines() 
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="retroedit",
    version="1.0.0",
    author="RetroEdit Team",
    author_email="retroedit@example.com",
    description="A retro-style text editor inspired by MS-DOS Edit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/retroedit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Editors",
        "Topic :: Terminals",
        "Environment :: Console :: Curses",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "retroedit=retroedit.main:main",
            "re=retroedit.main:main",
        ],
    },
    package_data={
        "retroedit": ["*.tcss"],
    },
    include_package_data=True,
)
