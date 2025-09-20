from typing import Generator
from tree_sitter import Language, Parser, Tree, Node
import tree_sitter_python as tspython
from collections import defaultdict

# Setup
PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

with open("example.py", "r", encoding="utf8") as f:
    code = f.read()

# Parse the code
tree = parser.parse(bytes(code, "utf8"))

def traverse_tree(tree: Tree, source_code: bytes) -> Generator[Node, None, None]:
    cursor = tree.walk()
    visited_children = False

    while True:
        if not visited_children:
            node = cursor.node
            node_text = source_code[node.start_byte:node.end_byte].decode("utf8")
            yield (node, node_text)
            if not cursor.goto_first_child():
                visited_children = True
        elif cursor.goto_next_sibling():
            visited_children = False
        elif not cursor.goto_parent():
            break

def get_parent_class(node: Node, source_code: bytes):
    parent = node.parent
    while parent:
        if parent.type == "class_definition":
            # The class name is the first child of type "identifier"
            for child in parent.children:
                if child.type == "identifier":
                    return source_code[child.start_byte:child.end_byte].decode("utf8")
        parent = parent.parent
    return None

if __name__ == "__main__":
    unique_types = set()
    nodes_by_type = defaultdict(list)
    functions = []

    for i, (node, node_text) in enumerate(traverse_tree(tree, bytes(code, "utf8")), start=1):
        nodes_by_type[node.type].append(node_text)
        unique_types.add(node.type)

        # If node is a function, store it with its parent class
        if node.type == "function_definition":
            parent_class = get_parent_class(node, bytes(code, "utf8"))
            functions.append((parent_class, node_text))

    # Print all unique node types
    print("Unique types:")
    for t in sorted(unique_types):
        print(t)

    # Print all functions with their parent class
    print("\nFunctions with parent class:")
    for parent_class, func_text in functions:
        if parent_class:
            print(f"\nClass: {parent_class}\nFunction:\n{func_text}\n{'-'*40}")
        else:
            print(f"\nFunction (module-level):\n{func_text}\n{'-'*40}")
