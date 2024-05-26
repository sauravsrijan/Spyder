# Supported languages

import tree_sitter_python as tspy
from tree_sitter import Language

# Maping of a language's extension with the respective Tree sitter language.
LANG_MAP = {
    "py": Language(tspy.language(), "python")
}
