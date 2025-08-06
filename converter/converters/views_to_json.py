import os
import sys
import json
import subprocess

from ast_utils import parse_python_file, extract_functions
from group_templates import group_functions, build_template
from ast_utils import unparse_functions

# Default JSON output file
JSON_OUTPUT_FILE = "controllers.json"

def build_json_only(group_map):
    json_map = {}

    for group, funcs in group_map.items():
        raw_code = unparse_functions(funcs)
        template = build_template(group, raw_code)
        json_map[f"{group}_controller"] = template

    return json_map

def main():
    if len(sys.argv) < 2:
        print("❌ Error: Please provide the path to the views Python file.")
        print("Usage: python -m converter.converters.views_to_json path/to/views_sample.py")
        sys.exit(1)

    VIEWS_FILE_PATH = sys.argv[1]

    if not os.path.exists(VIEWS_FILE_PATH):
        print(f"❌ File not found: {VIEWS_FILE_PATH}")
        sys.exit(1)

    tree = parse_python_file(VIEWS_FILE_PATH)
    func_nodes = extract_functions(tree)
    grouped = group_functions(func_nodes)
    json_map = build_json_only(grouped)

    with open(JSON_OUTPUT_FILE, "w") as out:
        json.dump(json_map, out, indent=2)

    print("✅ Controller templates written to JSON.")

    # Run gemini_converter using the same Python interpreter
    subprocess.run(
        [sys.executable, '-m', 'gemini_converter'],
        check=True,
        text=True
    )

if __name__ == "__main__":
    main()
