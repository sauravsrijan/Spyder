"""Spyder CLI."""
import os
import argparse

from collections import defaultdict

from engine import LANG_MAP
from engine.walker import Walker


def get_extension(file_path: str) -> str:
    """Return the extension of the file."""
    return file_path.split('.')[-1]


def main():
    """Spyder CLI."""
    parser = argparse.ArgumentParser(description='Spyder CLI')
    parser.add_argument('-f', '--file', type=str, help='File to spy on', default=None)
    parser.add_argument('-l', '--language', type=str, help='Language of the file', default='python')
    parser.add_argument('-d', '--directory', type=str, help='Directory to spy on', default=None)
    args = parser.parse_args()

    walker = Walker()

    ext_file_map = defaultdict(list)
    if args.file:
        extension = get_extension(args.file)
        ext_file_map[extension].append(args.file)

    if args.directory:
        # iterate the directory and get all files recursively
        for root, _, files in os.walk(args.directory):
            for file in files:
                extension = get_extension(file)
                ext_file_map[extension].append(os.path.join(root, file))

    for ext, files in ext_file_map.items():
        for file in files:
            print(f'Processing {file}...')
            walker.set_language(LANG_MAP[ext])
            tree = walker.get_tree_for_file(file)
            print("Parsed tree:", tree)


if __name__ == '__main__':
    main()
