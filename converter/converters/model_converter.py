# converter.py
import re
import os
import json

def map_field_type(field_line):
    """Maps Django field types to Mongoose/MERN stack data types."""
    mappings = {
        'CharField': 'String',
        'TextField': 'String',
        'UUIDField': 'String',
        'IntegerField': 'Number',
        'FloatField': 'Number',
        'BooleanField': 'Boolean',
        'DateTimeField': 'Date',
        'DateField': 'Date',
        'TimeField': 'String',
        'FileField': 'String',
        'ImageField': 'String',
        'EmailField': 'String',
        'URLField': 'String',
        'SlugField': 'String',
        'DecimalField': 'mongoose.Schema.Types.Decimal128', # More precise for Mongoose
        'PositiveIntegerField': 'Number',
        'PositiveSmallIntegerField': 'Number',
        'SmallIntegerField': 'Number',
        'BigIntegerField': 'Number',
        'JSONField': 'Object',
        'GenericIPAddressField': 'String',
        'DurationField': 'Number',
        'BinaryField': 'Buffer',
        'OneToOneField': 'mongoose.Schema.Types.ObjectId',
        'ForeignKey': 'mongoose.Schema.Types.ObjectId',
        'ManyToManyField': 'mongoose.Schema.Types.ObjectId',
    }
    for key, value in mappings.items():
        if f'models.{key}' in field_line:
            return value
    return 'String' # Default fallback

def convert_django_models_to_mongoose(django_model_path, output_dir):
    """
    Converts multiple Django models from a models.py file
    to separate Mongoose schemas in a specified output directory.
    """
    print(f"🚀 Starting conversion of '{django_model_path}'...")
    
    # --- Create Output Directory ---
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📂 Created output directory: '{output_dir}'")

    # --- Read and Pre-process Input File ---
    try:
        with open(django_model_path, 'r') as f:
            content = f.read()
            lines = content.splitlines()
    except FileNotFoundError:
        print(f"❌ ERROR: Input file not found at '{django_model_path}'")
        return

    # Pre-process to extract top-level variables like choice lists
    global_vars = {}
    try:
        # Execute file in a restricted scope to get variable values
        exec(content, global_vars)
    except Exception as e:
        print(f"⚠️ Warning: Could not execute models file to evaluate choice variables. Reason: {e}")

    # --- Main Parsing Logic ---
    all_models_data = []
    current_model_name = None
    current_model_fields = {}
    current_model_use_timestamps = False
    class_indentation = -1

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith('#'):
            continue

        line_indentation = len(line) - len(line.lstrip())

        # Detect start of a new Django Model class
        if line_stripped.startswith('class ') and '(models.Model)' in line_stripped:
            if current_model_name:
                all_models_data.append({
                    'name': current_model_name,
                    'fields': current_model_fields,
                    'timestamps': current_model_use_timestamps,
                })
            
            current_model_name = line_stripped.split('class ')[1].split('(')[0].strip()
            current_model_fields = {}
            current_model_use_timestamps = False
            class_indentation = line_indentation
            continue

        if current_model_name:
            # End of class definition based on indentation
            if line_indentation <= class_indentation:
                all_models_data.append({
                    'name': current_model_name,
                    'fields': current_model_fields,
                    'timestamps': current_model_use_timestamps,
                })
                current_model_name = None
                class_indentation = -1
                continue

            # Detect field definitions
            if '=' in line_stripped and 'models.' in line_stripped:
                name, rest = [x.strip() for x in line_stripped.split('=', 1)]
                
                # Ignore meta classes and other non-field attributes
                if name == 'Meta' or name.startswith('_'):
                    continue

                mongoose_field = {}
                django_type = map_field_type(rest)

                if "primary_key=True" in rest:
                    # Mongoose handles _id automatically, so we skip Django's primary keys
                    continue
                else:
                    mongoose_field['type'] = django_type

                if 'null=True' in rest or 'blank=True' in rest:
                    mongoose_field['required'] = False
                elif 'ForeignKey' in rest or 'OneToOneField' in rest or 'ManyToManyField' in rest:
                    if 'null=False' in rest:
                        mongoose_field['required'] = True
                else: 
                    mongoose_field['required'] = True

                # Default values
                default_match = re.search(r'default=([^,\)]+)', rest)
                if default_match:
                    default_val_str = default_match.group(1).strip()
                    if 'uuid.uuid4' in default_val_str:
                        mongoose_field['default'] = 'uuidv4'
                    elif 'timezone.now' in default_val_str:
                        mongoose_field['default'] = 'Date.now'
                    else:
                        try:
                            mongoose_field['default'] = eval(default_val_str)
                        except (NameError, SyntaxError):
                            mongoose_field['default'] = default_val_str.strip("'\"")

                if 'auto_now_add=True' in rest or 'auto_now=True' in rest:
                    current_model_use_timestamps = True
                    if name in ['created_at', 'updated_at', 'createdAt', 'updatedAt']:
                        continue 

                # Enum choices from variables
                choices_match = re.search(r'choices\s*=\s*([a-zA-Z0-9_]+)', rest)
                if choices_match:
                    choices_var_name = choices_match.group(1)
                    if choices_var_name in global_vars:
                        choices_list = global_vars[choices_var_name]
                        mongoose_field['enum'] = [choice[0] for choice in choices_list]

                if 'unique=True' in rest:
                    mongoose_field['unique'] = True

                if 'mongoose.Schema.Types.ObjectId' in mongoose_field.get('type', ''):
                    related_model_match = re.search(r"\((?:to=)?['\"]?([a-zA-Z0-9_.]+)['\"]?", rest)
                    if related_model_match:
                        related_model_name = related_model_match.group(1).split('.')[-1]
                        mongoose_field['ref'] = related_model_name.replace("'", "")

                    if 'ManyToManyField' in rest:
                        mongoose_field = [mongoose_field]
                    elif 'OneToOneField' in rest:
                        mongoose_field['unique'] = True
                
                if mongoose_field.get('required') is False:
                    del mongoose_field['required']
                    
                current_model_fields[name] = mongoose_field

    if current_model_name:
        all_models_data.append({
            'name': current_model_name,
            'fields': current_model_fields,
            'timestamps': current_model_use_timestamps,
        })

    # --- Generate Output Files ---
    for model_data in all_models_data:
        model_name = model_data['name']
        fields = model_data['fields']
        use_timestamps = model_data['timestamps']
        
        output_js_path = os.path.join(output_dir, f"{model_name}.js")

        with open(output_js_path, 'w') as out:
            out.write("const mongoose = require('mongoose');\n\n")
            out.write(f"const {model_name}Schema = new mongoose.Schema({{\n")
            
            for key, props in fields.items():
                out.write(f"  {key}: ")
                
                if isinstance(props, str):
                     out.write(f"{props},\n")
                     continue

                if isinstance(props, list):
                    field_def = json.dumps(props[0], indent=4)
                    out.write(f"[{field_def}],\n")
                else:
                    out.write(f"{json.dumps(props, indent=4)},\n")

            out.write("}" + (", { timestamps: true }" if use_timestamps else "") + ");\n\n")
            out.write(f"module.exports = mongoose.model('{model_name}', {model_name}Schema);\n")

        print(f"✅ Successfully converted '{model_name}' -> '{output_js_path}'")
    
    print("\n🎉 Conversion complete!")


# --- Main Execution Block ---
if __name__ == "__main__":
    # ⬇️ HARDCODE YOUR PATHS HERE ⬇️
    INPUT_FILE_PATH = "/Users/bharatvarma/code/Hackatons/Synchrony_Final/practice_folder/stackChange/converter/converters/Test_Cases/models.py"
    OUTPUT_DIRECTORY_PATH = "mern_models"
    
    # The main function is called with the hardcoded paths
    convert_django_models_to_mongoose(INPUT_FILE_PATH, OUTPUT_DIRECTORY_PATH)