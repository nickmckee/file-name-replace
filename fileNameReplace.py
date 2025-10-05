#!/usr/bin/env python3
import os
import sys
import argparse

def main():
    p = argparse.ArgumentParser(
        description="Rename files under a directory by replacing literal text in file names."
    )
    p.add_argument("search", help="Search text - text to be replaced")
    p.add_argument("replace", help="Replacement text - text to replace with")
    p.add_argument("--dir", default=".", help="Execution directory (and sub-directories)")
    p.add_argument("--dry-run", action="store_true", help="Preview the change - show before and after file name changes")
    p.add_argument(
        "--skip",
        default=".git,.idea,node_modules",
        help="Comma-separated folder names to skip",
    )
    args = p.parse_args()

    base_dir = os.path.abspath(args.dir)
    if not os.path.isdir(base_dir):
        print(f"Error: --dir path is not a directory: {base_dir}")
        sys.exit(2)

    skip_names = set(s.strip() for s in args.skip.split(",") if s.strip())

    for dirpath, dirnames, filenames in os.walk(base_dir, topdown=True):
        # remove skipped dirs from traversal
        dirnames[:] = [d for d in dirnames if d not in skip_names]

        for name in filenames:
            if args.search in name:
                old = os.path.join(dirpath, name)
                new_name = name.replace(args.search, args.replace)
                if new_name != name:
                    new = os.path.join(dirpath, new_name)

                    # Output: base names only (extensions removed)
                    old_base, _ = os.path.splitext(name)
                    new_base, _ = os.path.splitext(new_name)
                    print(f"{old_base}  ->  {new_base}")

                    if not args.dry_run:
                        os.rename(old, new)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: fileNameReplace <search> <replace> [--dir PATH] [--dry-run] [--skip names]")
        sys.exit(1)
    main()
