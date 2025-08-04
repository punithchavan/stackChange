import os
import json
from .ast_utils import parse_python_file, extract_functions
from .group_templates import group_functions, build_template
from .ast_utils import unparse_functions

VIEWS_FILE_PATH = "backend/sample_views.py"
OUTPUT_DIR = "temp_controllers"
JSON_OUTPUT_FILE = "controllers.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def write_grouped_templates(group_map):
    json_map = {}

    for group, funcs in group_map.items():
        raw_code = unparse_functions(funcs)
        template = build_template(group, raw_code)

        # Save to .js file
        path = os.path.join(OUTPUT_DIR, f"{group}.controller.js")
        with open(path, "w") as f:
            f.write(template)

        # Add to JSON for Gemini
        json_map[f"{group}_controller"] = template

    return json_map

def main():
    tree = parse_python_file(VIEWS_FILE_PATH)
    func_nodes = extract_functions(tree)
    grouped = group_functions(func_nodes)
    json_map = write_grouped_templates(grouped)

    with open(JSON_OUTPUT_FILE, "w") as out:
        json.dump(json_map, out, indent=2)

    print("Views converted to controller templates and JSON ready.")

if __name__ == "__main__":
    main()
