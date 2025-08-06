import os
import json
import datetime
import google.generativeai as genai

from dotenv import load_dotenv
from group_templates import generate_controller_templates  # 👈 integrates templates

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
def convert_all_views(nested_views_dict: dict):
    """
    Accepts input from views_to_json.py and reformats it:

    Input: Dict like:
    {
        "user_controller": {
            "get_user": "def get_user(...):",
            "post_comment": "def post_comment(...):"
        },
        ...
    }

    Converts to:
    {
        "user_controller": {
            "get_user": "converted JS code",
            ...
        }
    }

    Then passes to generate_controller_templates.
    """
    result = {}
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(LOG_DIR, f"log_{timestamp}.json")
    log_data = []

    for controller_name, view_dict in nested_views_dict.items():
        result[controller_name] = {}
        for func_name, source_code in view_dict.items():
            converted = call_gemini_api(source_code)

            result[controller_name][func_name] = converted

            log_data.append({
                "controller": controller_name,
                "name": func_name,
                "input": source_code,
                "output": converted
            })

    # Save logs
    with open(log_path, "w") as log_file:
        json.dump(log_data, log_file, indent=2)

    # ✅ Generate controller templates
    generate_controller_templates(result)

    return result
