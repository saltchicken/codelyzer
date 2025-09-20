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

def walk_tree(tree):
    cursor = tree.walk()
    print(cursor.node.type) # module
    cursor.goto_first_child()
    # print(f"First child type: {cursor.node.type}")  # Output: function_definition
    print(cursor.node.text.decode("utf8"))


def traverse_tree(tree: Tree) -> Generator[Node, None, None]:
    cursor = tree.walk()
    visited_children = False

    while True:
        if not visited_children:
            node = cursor.node
            node_text = node.text.decode("utf8")
            yield (node.type, node_text)
            if not cursor.goto_first_child():
                visited_children = True
        elif cursor.goto_next_sibling():
            visited_children = False
        elif not cursor.goto_parent():
            break

def test_root_node():
    # Inspect the root node
    root_node = tree.root_node
    function_node = root_node.children[0]
    print(f"First child type: {function_node.type}")  # Output: function_definition

    name_node = function_node.child_by_field_name("name")
    print(f"Function name: {name_node.text.decode('utf8')}")  # Output: greet

    body_node = function_node.child_by_field_name("body")

    print(f"Body type: {body_node.type}")  # Output: block
    call_node = body_node.children[0].children[0]
    print(call_node.type)
    # print(f"Call function: {call_node.child_by_field_name('function').text.decode('utf8')}")  # Output: print

def print_nodes_of_type(node_type: str):
    if node_type not in nodes_by_type:
        print(f"No nodes of type {node_type}")
        return

    print(f"Nodes of type {node_type}:")
    for node_text in nodes_by_type[node_type]:
        print(node_text)

if __name__ == "__main__":
    unique_types = set()
    nodes_by_type = defaultdict(list)

    for i, (node_type, node_text) in enumerate(traverse_tree(tree), start=1):
        # print(f"{i}: Type:{node_type} \nText:{node_text!r}")
        nodes_by_type[node_type].append(node_text)

        unique_types.add(node_type)


    # for t in sorted(unique_types):
    #     print(t)
    #
    print_nodes_of_type("function_definition")
