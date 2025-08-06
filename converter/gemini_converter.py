import os
import json
import datetime
import google.generativeai as genai

from dotenv import load_dotenv
from group_templates import build_template  # 🧠 old template generator
from views_to_json import write_grouped_templates  # 🧠 for grouped views
from ast_utils import unparse_functions, parse_python_file, extract_functions, group_functions  # 🧠 AST utilities

load_dotenv()

# 🔑 Set Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 📁 Ensure output and logs directories exist
OUTPUT_DIR = os.path.join("converter", "converted", "views")
LOG_DIR = os.path.join("converter", "conversion_logs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ✨ Prompt Template
def make_prompt(source_code: str) -> str:
    return f"""
Convert the following Django view function to an Express.js controller function using modern syntax:

Django View:
```python
{source_code}
```

Express.js Controller:
"""

# 🚀 Gemini Flash Call
def call_gemini_api(source_code: str) -> str:
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = make_prompt(source_code)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# 🧠 Convert Views in Grouped Controller Structure
def convert_all_views(django_views_path):
    """
    Input: Path to views.py file
    Output: Creates converted .controller.js files in OUTPUT_DIR
    """
    # Get grouped views from AST
    tree = parse_python_file(django_views_path)
    func_nodes = extract_functions(tree)
    grouped_views = group_functions(func_nodes)  # {group: [func1, func2, ...]}

    result = {}
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(LOG_DIR, f"log_{timestamp}.json")
    log_data = []

    for group_name, func_nodes in grouped_views.items():
        raw_code = unparse_functions(func_nodes)  # convert AST to raw Django code
        template = build_template(group_name, raw_code)  # generate template string
        converted = call_gemini_api(template)

        # Save final controller file
        output_path = os.path.join(OUTPUT_DIR, f"{group_name}.controller.js")
        with open(output_path, "w") as f:
            f.write(converted)

        # For logs
        result[group_name] = converted
        log_data.append({
            "controller": group_name,
            "input_template": template,
            "output": converted
        })

    # Save logs
    with open(log_path, "w") as log_file:
        json.dump(log_data, log_file, indent=2)

    return result

# 🧪 Example usage
if __name__ == "__main__":
    path_to_views = "backend/sample_views.py"  # replace with actual path
    convert_all_views(path_to_views)
