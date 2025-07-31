import os
import json
import datetime
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()  # 👈 this loads variables from .env


# 🔑 Set your Gemini API key (make sure GEMINI_API_KEY is in your environment variables)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 📁 Ensure logs directory exists
LOG_DIR = "conversion_logs"
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

# 🧠 Convert All Views in a Batch
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

        log_data.append({
            "name": name,
            "input": code,
            "output": converted
        })

    # Save logs
    with open(log_path, "w") as log_file:
        json.dump(log_data, log_file, indent=2)

    return result
