from tree_sitter import Language, Parser, Node, Tree

from typing import Generator


class Walker:
    def __init__(self) -> None:
        self.parser = Parser()

    @staticmethod
    def get_language(path_or_ptr: str | int, name: str) -> Language:
        """Return the language of the parser."""
        return Language(path_or_ptr, name)

    def set_language(self, language: Language) -> None:
        """Set the language for the parser."""
        self.parser.set_language(language)

    def get_tree(self, code: str, encoding: str = 'utf-8') -> Tree:
        """Given a code, return the AST of the code."""
        tree = self.parser.parse(bytes(code, encoding))
        return tree

    def get_tree_for_file(self, file_path: str, encoding: str = 'utf-8') -> Tree:
        """Given a file path, return the AST of the file."""
        # skipcq: PTC-W6004: Nothing sensitive happening here.
        with open(file_path, 'r') as file:
            code = file.read()
        return self.get_tree(code, encoding)

    @staticmethod
    def traverse_tree(tree: Tree) -> Generator[Node, None, None]:
        cursor = tree.walk()

        visited_children = False
        while True:
            if not visited_children:
                yield cursor.node
                if not cursor.goto_first_child():
                    visited_children = True
            elif cursor.goto_next_sibling():
                visited_children = False
            elif not cursor.goto_parent():
                break
