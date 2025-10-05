# file-name-replace

A lightweight command-line utility for doing search and find replace of all file names in the current or otherwise specified directory. 

--------
Overview
--------
- Find and replace rename of files
- Works recursively through all subfolders  
- Supports a preview mode to see changes before committing
- Use in current directory or a specified directory
- Include a list of comma separated directory you would like to skip execution for



-------------
 Installation
-------------

1. Install Python 3.10 or later (https://www.python.org/downloads/)

2. Download this repository into a location of your choosing

3. For windows add the optional wrapper to call the command from anywhere by running the command from the file-name-replace directory

@echo off
python "%~dp0fileNameReplace.py" %*



----------------
Using the script
----------------
From the the intended directory (or include the intended directory for the Path) run:

fileNameReplace <search> <replace> [--dir PATH] [--dry-run] [--skip /SkipDirectory1, etc..,]



----------
Arguements
----------
| Argument     | Description                                                                                
| ------------------------------------------------------------------------|
| `<search>`   | Literal text to find in file names                                                         |
| `<replace>`  | Literal text to replace it with                                                            |
| `--dir PATH` | Directory to operate in (default: current directory `.`)                                   |
| `--dry-run`  | Preview changes without renaming                                                           |
| `--skip`     | Comma-separated folder names to skip during traversal 



