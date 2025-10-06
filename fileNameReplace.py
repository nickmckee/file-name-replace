#!/usr/bin/env python3
import os
import sys
import argparse
from collections import defaultdict


def will_change(old_path, new_path):
    """Return True only if the basename would change."""
    return os.path.basename(old_path) != os.path.basename(new_path)

def print_map(old_path, new_path):
    """Print OldBase -> NewBase (extensions removed), only when change occurs."""
    old_base, _ = os.path.splitext(os.path.basename(old_path))
    new_base, _ = os.path.splitext(os.path.basename(new_path))
    if old_base != new_base:
        print(f"{old_base}  ->  {new_base}")


def cmd_replace(args):
    base_dir = os.path.abspath(args.dir)
    if not os.path.isdir(base_dir):
        print(f"Error: --dir path is not a directory: {base_dir}")
        sys.exit(2)

    skip_names = set(s.strip() for s in args.skip.split(",") if s.strip())
    count = 0

    for dirpath, dirnames, filenames in os.walk(base_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in skip_names]

        for name in filenames:
            if args.search not in name:
                continue

            old = os.path.join(dirpath, name)
            new_name = name.replace(args.search, args.replace)
            new = os.path.join(dirpath, new_name)

            if will_change(old, new):
                print_map(old, new)
                count += 1
                if not args.dry_run:
                    os.rename(old, new)

    # Summary
    if count == 0:
        print("\nNo files would change.")
    else:
        action = "would change" if args.dry_run else "renamed"
        print(f"\nSummary: {count} file{'s' if count != 1 else ''} {action}.")


def safe_pivot_suffix(name, pivot):
    """Return the substring starting at the pivot (inclusive).
    If there's a single space immediately before the pivot, include it (keeps ' - ')."""
    idx = name.find(pivot)
    if idx < 0:
        return None
    start = idx
    if idx > 0 and name[idx - 1] == " ":
        start = idx - 1
    return name[start:]  # includes pivot (and maybe preceding space)

def substitute_phrase(phrase, i_val, j_val, pad):
    """Replace %i% and %j% tokens in phrase."""
    si = str(i_val).zfill(pad)
    sj = str(j_val).zfill(pad)
    return phrase.replace("%i%", si).replace("%j%", sj)

def collect_groups(base_dir, skip_names, pivot):
    """Walk recursively and collect files that CONTAIN the pivot, grouped by parent directory."""
    groups = defaultdict(list)
    parents = set()

    for dirpath, dirnames, filenames in os.walk(base_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in skip_names]
        pivot_files = [f for f in filenames if pivot in f]
        if pivot_files:
            parents.add(dirpath)
            groups[dirpath].extend(pivot_files)

    parent_dirs = sorted(parents, key=lambda p: os.path.relpath(p, base_dir).lower())
    for p in parent_dirs:
        groups[p] = sorted(groups[p], key=lambda n: n.lower())
    return parent_dirs, groups

def cmd_iterate(args):
    base_dir = os.path.abspath(args.dir)
    if not os.path.isdir(base_dir):
        print(f"Error: --dir path is not a directory: {base_dir}")
        sys.exit(2)

    phrase = args.phrase
    pivot  = args.pivot
    pad    = args.pad
    skip_names = set(s.strip() for s in args.skip.split(",") if s.strip())

    if ("%i%" not in phrase) and ("%j%" not in phrase):
        print("Warning: phrase contains neither %i% nor %j%; proceeding without indices.")

    parent_dirs, groups = collect_groups(base_dir, skip_names, pivot)
    count = 0

    # j = folder iterator (1-based)
    for j_idx, parent in enumerate(parent_dirs, start=1):
        files = groups[parent]
        # i = file iterator within folder (1-based)
        for i_idx, name in enumerate(files, start=1):
            suffix = safe_pivot_suffix(name, pivot)
            if suffix is None:
                continue

            lead = substitute_phrase(phrase, i_idx, j_idx, pad)
            base_no_ext, ext = os.path.splitext(name)

            new_base_with_suffix = lead + suffix
            new_name = os.path.splitext(new_base_with_suffix)[0] + ext

            old_path = os.path.join(parent, name)
            new_path = os.path.join(parent, new_name)

            if will_change(old_path, new_path):
                print_map(old_path, new_path)
                count += 1
                if not args.dry_run:
                    os.rename(old_path, new_path)

    # Summary
    if count == 0:
        print("\nNo files would change.")
    else:
        action = "would change" if args.dry_run else "renamed"
        print(f"\nSummary: {count} file{'s' if count != 1 else ''} {action}.")

def build_parser():
    p = argparse.ArgumentParser(
        description="Rename utilities: (1) literal replace, (2) iterator-based rename before pivot. Files only."
    )
    sub = p.add_subparsers(dest="command", required=True)

    # replace
    pr = sub.add_parser("replace", help="Literal substring replacement in file names (recursive).")
    pr.add_argument("search", help="Literal text to find in file names")
    pr.add_argument("replace", help="Literal text to replace it with")
    pr.add_argument("--dir", default=".", help="Directory to run in (default: current directory)")
    pr.add_argument("--dry-run", action="store_true", help="Preview only; print only items that would change")
    pr.add_argument("--skip", default=".git,.idea,node_modules",
                    help="Comma-separated folder names to skip (default: .git,.idea,node_modules)")
    pr.set_defaults(func=cmd_replace)

    # iterate
    pi = sub.add_parser("iterate", help="Replace everything BEFORE a pivot with a phrase using %i% (file) and %j% (folder) iterators.")
    pi.add_argument("--pivot", required=True, help="Literal pivot (e.g., '-') — everything before the FIRST pivot is replaced.")
    pi.add_argument("--phrase", required=True, help="Phrase with %i% and/or %j% placeholders (e.g., 's%i%e%j').")
    pi.add_argument("--pad", type=int, default=2, help="Zero-padding for iterators (default: 2 → 01, 02, ...)")
    pi.add_argument("--dir", default=".", help="Directory to run in (default: current directory)")
    pi.add_argument("--dry-run", action="store_true", help="Preview only; print only items that would change")
    pi.add_argument("--skip", default=".git,.idea,node_modules",
                    help="Comma-separated folder names to skip (default: .git,.idea,node_modules)")
    pi.set_defaults(func=cmd_iterate)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage:\n"
              "  fileNameReplace replace <search> <replace> [--dir PATH] [--dry-run] [--skip names]\n"
              "  fileNameReplace iterate --pivot P --phrase PHRASE [--pad N] [--dir PATH] [--dry-run] [--skip names]")
        sys.exit(1)
    main()
