# file-name-replace

A lightweight command-line utility for doing search and find replace of all file names in the current or otherwise specified directory. 



--------
Overview
--------
1. **replace** — literal substring replacement in file names.  
2. **iterate** — replace everything **before a pivot** with a formatted string using iterators:
   - `%j` = folder index (per parent folder, sorted by path)
   - `%i` = file index (per folder, sorted by file name)

Both modes work recursively, operate on **files only**, and support a **dry run**.



-------------
 Installation
-------------

1. Install Python 3.10 or later (https://www.python.org/downloads/)

2. Download this repository into a location of your choosing

3. For windows add the optional wrapper to call the command from anywhere by running the command from the file-name-replace directory

@echo off
python "%~dp0fileNameReplace.py" %*

Make sure to add the folder to your Path variable so cmd/powershell/ect can pick up the command.



----------------
Using the script
----------------
From the intended directory (or include the intended directory for the Path) run:


fileNameReplace replace <search> <replace> [--dir PATH] [--dry-run] [--skip name1,name2,...]

<search>: literal text to find in file names
<replace>: literal text to replace it with
--dir PATH: where to run (default: current directory)
--dry-run: preview only
--skip: comma-separated folder names to skip (default: .git,.idea,node_modules)


Examples:

fileNameReplace replace "old" "new" --dry-run
fileNameReplace replace "old" "new"
fileNameReplace replace " - Copy" "" --dir "P:\Downloads"


*********************************************************

fileNameReplace iterate --pivot "-" --phrase "SEASON_%i%_EPISODE_%j%" [--pad 2] [--dir PATH] [--dry-run] [--skip names]

--pivot – literal text to split the name; everything before the first occurrence is replaced
--phrase – your label template with %i% and/or %j% placeholders
--pad – digits to pad both iterators (default 2)
--dir PATH: where to run (default: current directory)
--dry-run: preview only
--skip: comma-separated folder names to skip (default: .git,.idea,node_modules)

Exmaples:

fileNameReplace iterate --pivot "-" --phrase "s%i%e%j%" --pad 2 --dir "P:\Shows" --dry-run

BlahBlahBlah - SomethingSomething -> s01e01 - SomethingSomething



