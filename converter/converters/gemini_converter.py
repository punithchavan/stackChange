import os
import json
import datetime
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

# 🔑 Set Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 🗁 Ensure output and logs directories exist
OUTPUT_DIR = os.path.join("media/output_project")  # <- Updated to output to "controller" folder
LOG_DIR = os.path.join("converter", "conversion_logs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ✨ Prompt Template
def make_prompt(source_code: str) -> str:
    return f"""
Convert the following Django view function to an Express.js controller function using modern syntax. Return only clean JavaScript code. No markdown, no comments, no explanation.

Django View:
{source_code}

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

# 🧐 Convert from JSON Template to Final JS Controllers
def convert_from_json_template(json_path):
    with open(json_path, "r") as f:
        controller_map = json.load(f)

    result = {}
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(LOG_DIR, f"log_{timestamp}.json")
    log_data = []

    for controller_name, template_code in controller_map.items():
        # Extract commented Django functions from the template
        lines = template_code.split("\n")
        extracted_funcs = []
        buffer = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("// def "):
                if buffer:
                    extracted_funcs.append("\n".join(buffer))
                    buffer = []
                buffer.append(stripped[3:].strip())
            elif buffer and stripped.startswith("//"):
                buffer.append(stripped[3:].strip())
            elif buffer:
                extracted_funcs.append("\n".join(buffer))
                buffer = []

        if buffer:
            extracted_funcs.append("\n".join(buffer))

        # Convert each function and combine output (de-duplicate headers)
        generated_parts = []
        for func in extracted_funcs:
            converted = call_gemini_api(func)
            generated_parts.append(converted.strip())

        body_lines = []
        for part in generated_parts:
            cleaned = []
            for line in part.splitlines():
                line = line.strip()
                if line.startswith("```"):
                    continue
                if line in [
                    "const express = require('express');",
                    "const router = express.Router();",
                    "module.exports = router;"
                ]:
                    continue
                cleaned.append(line)
            body_lines.extend(cleaned)

        controller_code = "const express = require('express');\nconst router = express.Router();\n"
        controller_code += "\n".join(body_lines)
        controller_code += "\n\nmodule.exports = router;"

        # Save final file
        output_path = os.path.join(OUTPUT_DIR, f"{controller_name}.js")
        with open(output_path, "w") as f:
            f.write(controller_code)

        result[controller_name] = controller_code
        log_data.append({
            "controller": controller_name,
            "input_template": template_code,
            "output": controller_code
        })

    with open(log_path, "w") as log_file:
        json.dump(log_data, log_file, indent=2)

    return result

# 🥪 Example usage
if __name__ == "__main__":
    path_to_json = "controllers.json"  # <- Ensure this matches your filename
    convert_from_json_template(path_to_json)
