import ast

def parse_python_file(filepath):
    with open(filepath, "r") as f:
        return ast.parse(f.read())

def extract_functions(tree):
    return [node for node in tree.body if isinstance(node, ast.FunctionDef)]

def unparse_functions(func_nodes):
    return "\n\n".join([ast.unparse(f) for f in func_nodes])