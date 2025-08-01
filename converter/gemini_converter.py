import os
import json
import datetime
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()  

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

OUTPUT_DIR = os.path.join("converter", "converted", "views")
LOG_DIR = os.path.join("converter", "conversion_logs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

def make_prompt(source_code: str) -> str:
    return f"""
Convert the following Django view function to an Express.js controller function using modern syntax:

Django View:
```python
{source_code}
```

Express.js Controller:
"""

def call_gemini_api(source_code: str) -> str:
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    prompt = make_prompt(source_code)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def convert_all_views(view_list):
    """
    Input: List of dicts with 'name' and 'source_code'
    Output: Dict with name → converted Express.js code
    """
    result = {}
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(LOG_DIR, f"log_{timestamp}.json")
    log_data = []

    for view in view_list:
        name = view.get("name", "unknown")
        code = view.get("source_code", "")
        converted = call_gemini_api(code)

        result[name] = converted

        # Write converted JS file
        safe_name = name.replace(".py", "").replace("/", "_")
        out_path = os.path.join(OUTPUT_DIR, f"{safe_name}.js")
        with open(out_path, "w") as f:
            f.write(converted)

        # Append to log
        log_data.append({
            "name": name,
            "input": code,
            "output_file": out_path,
            "output": converted
        })

    # Save logs
    with open(log_path, "w") as log_file:
        json.dump(log_data, log_file, indent=2)

    return result
