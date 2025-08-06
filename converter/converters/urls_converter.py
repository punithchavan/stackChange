
# import re
# import os
# from collections import defaultdict

# def convert_django_urls_to_express(input_path, output_path):
#     print(f"🚀 Starting conversion of '{input_path}'...")

#     try:
#         with open(input_path, 'r') as f:
#             content = f.read()
#     except FileNotFoundError:
#         print(f"❌ ERROR: Input file not found at '{input_path}'")
#         return

#     urlpatterns_match = re.search(r'urlpatterns\s*=\s*\[(.*?)\]', content, re.DOTALL)
#     if not urlpatterns_match:
#         print("❌ ERROR: Could not find 'urlpatterns' list in the file.")
#         return

#     urlpatterns_content = urlpatterns_match.group(1)
#     path_matches = re.findall(r"path\((.*?)\)", urlpatterns_content, re.DOTALL)

#     generated_routes = []
#     controller_map = defaultdict(list)

#     for match in path_matches:
#         parts = [p.strip() for p in match.split(',')]
#         django_path = parts[0].strip("'\"")
#         express_path = f"/{re.sub(r'<[^:]+:(\w+)>', r':\1', django_path)}"

#         view_part_cleaned = parts[1].replace('.as_view()', '')
#         view_name_match = re.search(r'views\.(\w+)', view_part_cleaned)
#         if not view_name_match:
#             continue
#         view_name = view_name_match.group(1)

#         controller_file = "genericController"
#         if "product" in view_name.lower():
#             controller_file = "productController"
#         elif "order" in view_name.lower():
#             controller_file = "orderController"
#         elif "auth" in view_name.lower():
#             controller_file = "authController"
#         elif "user" in view_name.lower():
#             controller_file = "userController"

#         is_detail_route = bool(re.search(r':\w+/?$', express_path))
        
#         # <-- FIX 1: Add .replace('_view', '') to properly clean all view names.
#         base_name = view_name.replace('View', '').replace('Detail', '').replace('List', '').replace('_view', '')

#         if is_detail_route:
#             get_one_func = f"get{base_name}"
#             update_func = f"update{base_name}"
#             delete_func = f"delete{base_name}"
            
#             generated_routes.append(f"router.get('{express_path}', {get_one_func});")
#             generated_routes.append(f"router.put('{express_path}', {update_func});")
#             generated_routes.append(f"router.delete('{express_path}', {delete_func});")
#             controller_map[controller_file].extend([get_one_func, update_func, delete_func])
#         else:
#             get_all_func = f"get{base_name}s"
#             create_func = f"create{base_name}"
            
#             # <-- FIX 2: Use the variable {create_func} in the f-string, not the literal 'create_func'.
#             if "login" in base_name.lower() or "logout" in base_name.lower():
#                  generated_routes.append(f"router.post('{express_path}', {create_func});")
#             else:
#                 generated_routes.append(f"router.get('{express_path}', {get_all_func});")
#                 generated_routes.append(f"router.post('{express_path}', {create_func});")

#             controller_map[controller_file].extend([get_all_func, create_func])

#     output_dir = os.path.dirname(output_path)
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
        
#     with open(output_path, 'w') as f:
#         f.write("const express = require('express');\nconst router = express.Router();\n\n")
#         f.write("// Import Controller Functions\n")
#         for controller, functions in sorted(controller_map.items()):
#             unique_functions = sorted(list(set(functions)))
#             f.write(f"const {{\n  {',\n  '.join(unique_functions)}\n}} = require('../controllers/{controller}');\n\n")
        
#         f.write("// --- API Routes ---\n")
#         for route in sorted(generated_routes):
#             f.write(f"{route}\n")

#         f.write("\nmodule.exports = router;\n")

#     print(f"✅ Successfully converted '{input_path}' -> '{output_path}'")

# # --- Main Execution Block ---
# if __name__ == "__main__":
#     INPUT_URLS_FILE = "/Users/bharatvarma/code/Hackatons/Synchrony_Final/practice_folder/stackChange/converter/converters/Test_Cases/urls2.py"
#     OUTPUT_ROUTER_FILE = "mern_routes/apiRoutes.js"
#     convert_django_urls_to_express("urls.py", OUTPUT_ROUTER_FILE)



# # ast_converter.py
# import ast
# import re
# import os
# from collections import defaultdict

# class ViewParser(ast.NodeVisitor):
#     """
#     Parses a views.py file to find which model is associated with each
#     class-based view.
#     """
#     def __init__(self):
#         self.view_to_model = {}
#         self.current_class = None

#     def visit_ClassDef(self, node):
#         self.current_class = node.name
#         # Look for the model attribute inside the class body
#         for item in node.body:
#             if isinstance(item, ast.Assign):
#                 # Check if the assignment is for the 'model' attribute
#                 if len(item.targets) == 1 and isinstance(item.targets[0], ast.Name) and item.targets[0].id == 'model':
#                     if isinstance(item.value, ast.Name):
#                         model_name = item.value.id
#                         self.view_to_model[self.current_class] = model_name
#         self.current_class = None

# class URLParser(ast.NodeVisitor):
#     """
#     Parses a urls.py file and uses the view-to-model mapping to
#     generate Express routes.
#     """
#     def __init__(self, view_to_model_map):
#         self.view_to_model = view_to_model_map
#         self.generated_routes = []
#         self.controller_map = defaultdict(list)

#     def visit_Assign(self, node):
#         # Find the 'urlpatterns = [...]' assignment
#         if len(node.targets) == 1 and node.targets[0].id == 'urlpatterns':
#             # The value should be a list of path() calls
#             if isinstance(node.value, ast.List):
#                 for call_node in node.value.elts:
#                     if isinstance(call_node, ast.Call) and call_node.func.id == 'path':
#                         self._process_path_call(call_node)

#     def _process_path_call(self, node):
#         if not node.args:
#             return

#         # 1. Get Route Path
#         django_path = node.args[0].value
#         express_path = f"/{re.sub(r'<[^:]+:(\w+)>', r':\1', django_path)}"

#         # 2. Get View Name
#         view_node = node.args[1]
#         view_name = None
#         if isinstance(view_node, ast.Attribute) and view_node.value.id == 'views':
#              # For function-based views like 'views.my_view'
#             view_name = view_node.attr
#         elif isinstance(view_node, ast.Call) and view_node.func.attr == 'as_view':
#             # For class-based views like 'views.MyView.as_view()'
#             if hasattr(view_node.func.value, 'attr'):
#                 view_name = view_node.func.value.attr # e.g., 'PostListView'
        
#         if not view_name:
#             return

#         # 3. Determine Controller File using the AST-generated map
#         model_name = self.view_to_model.get(view_name)
#         if model_name:
#             controller_file = f"{model_name.lower()}Controller"
#         else:
#             # Fallback for function-based views or views without a model attribute
#             controller_file = "genericController"

#         # 4. Generate RESTful routes (logic reused from previous script)
#         is_detail_route = bool(re.search(r':\w+/?$', express_path))
#         base_name = view_name.replace('View', '').replace('Detail', '').replace('List', '').replace('_view', '')

#         if is_detail_route:
#             get_one_func = f"get{base_name}"
#             update_func = f"update{base_name}"
#             delete_func = f"delete{base_name}"
            
#             self.generated_routes.append(f"router.get('{express_path}', {get_one_func});")
#             self.generated_routes.append(f"router.put('{express_path}', {update_func});")
#             self.generated_routes.append(f"router.delete('{express_path}', {delete_func});")
#             self.controller_map[controller_file].extend([get_one_func, update_func, delete_func])
#         else:
#             get_all_func = f"get{base_name}s"
#             create_func = f"create{base_name}"
            
#             self.generated_routes.append(f"router.get('{express_path}', {get_all_func});")
#             self.generated_routes.append(f"router.post('{express_path}', {create_func});")
#             self.controller_map[controller_file].extend([get_all_func, create_func])


# def convert_urls_with_ast(urls_path, views_path, output_path):
#     """Main function to drive the AST-based conversion."""
#     print("🧠 Analyzing views.py with AST to map views to models...")
#     try:
#         with open(views_path, 'r') as f:
#             views_content = f.read()
#         views_tree = ast.parse(views_content)
#         view_parser = ViewParser()
#         view_parser.visit(views_tree)
#         view_to_model_map = view_parser.view_to_model
#         print(f"✅ Found model mappings: {view_to_model_map}")
#     except FileNotFoundError:
#         print(f"❌ ERROR: Views file not found at '{views_path}'")
#         return

#     print(f"🚀 Converting '{urls_path}' using model mappings...")
#     try:
#         with open(urls_path, 'r') as f:
#             urls_content = f.read()
#         urls_tree = ast.parse(urls_content)
#         url_parser = URLParser(view_to_model_map)
#         url_parser.visit(urls_tree)
#     except FileNotFoundError:
#         print(f"❌ ERROR: URLs file not found at '{urls_path}'")
#         return

#     # Write the output file
#     output_dir = os.path.dirname(output_path)
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
        
#     with open(output_path, 'w') as f:
#         f.write("const express = require('express');\nconst router = express.Router();\n\n")
#         f.write("// Import Controller Functions (grouped by model)\n")
#         for controller, functions in sorted(url_parser.controller_map.items()):
#             unique_functions = sorted(list(set(functions)))
#             f.write(f"const {{\n  {',\n  '.join(unique_functions)}\n}} = require('../controllers/{controller}');\n\n")
        
#         f.write("// --- API Routes ---\n")
#         for route in sorted(url_parser.generated_routes):
#             f.write(f"{route}\n")
#         f.write("\nmodule.exports = router;\n")

#     print(f"✅ Successfully created '{output_path}'")


# if __name__ == "__main__":
#     # --- Configuration ---
#     # The script now needs to know where your views.py file is.
#     INPUT_URLS_FILE = "/Users/bharatvarma/code/Hackatons/Synchrony_Final/practice_folder/stackChange/converter/converters/Test_Cases/urls2.py"
#     INPUT_VIEWS_FILE = "/Users/bharatvarma/code/Hackatons/Synchrony_Final/practice_folder/stackChange/converter/converters/Test_Cases/views.py"
#     OUTPUT_ROUTER_FILE = "mern_routes/apiRoutes.js"
    
#     convert_urls_with_ast(INPUT_URLS_FILE, INPUT_VIEWS_FILE, OUTPUT_ROUTER_FILE)


# import ast
# import re
# import os
# import sys
# from collections import defaultdict

# class ViewParser(ast.NodeVisitor):
#     def __init__(self):
#         self.view_to_model = {}
#         self.current_class = None

#     def visit_ClassDef(self, node):
#         self.current_class = node.name
#         for item in node.body:
#             if isinstance(item, ast.Assign):
#                 if len(item.targets) == 1 and isinstance(item.targets[0], ast.Name) and item.targets[0].id == 'model':
#                     if isinstance(item.value, ast.Name):
#                         model_name = item.value.id
#                         self.view_to_model[self.current_class] = model_name
#         self.current_class = None

# class URLParser(ast.NodeVisitor):
#     def __init__(self, view_to_model_map):
#         self.view_to_model = view_to_model_map
#         self.generated_routes = []
#         self.controller_map = defaultdict(list)

#     def visit_Assign(self, node):
#         if len(node.targets) == 1 and getattr(node.targets[0], 'id', None) == 'urlpatterns':
#             if isinstance(node.value, ast.List):
#                 for call_node in node.value.elts:
#                     if isinstance(call_node, ast.Call) and getattr(call_node.func, 'id', '') == 'path':
#                         self._process_path_call(call_node)

#     def _process_path_call(self, node):
#         if not node.args:
#             return

#         django_path = node.args[0].value
#         express_path = f"/{re.sub(r'<[^:]+:(\w+)>', r':\1', django_path)}"

#         view_node = node.args[1]
#         view_name = None
#         if isinstance(view_node, ast.Attribute) and view_node.value.id == 'views':
#             view_name = view_node.attr
#         elif isinstance(view_node, ast.Call) and view_node.func.attr == 'as_view':
#             if hasattr(view_node.func.value, 'attr'):
#                 view_name = view_node.func.value.attr

#         if not view_name:
#             return

#         model_name = self.view_to_model.get(view_name)
#         if model_name:
#             controller_file = f"{model_name.lower()}Controller"
#         else:
#             controller_file = "genericController"

#         is_detail_route = bool(re.search(r':\w+/?$', express_path))
#         base_name = view_name.replace('View', '').replace('Detail', '').replace('List', '').replace('_view', '')

#         if is_detail_route:
#             get_one_func = f"get{base_name}"
#             update_func = f"update{base_name}"
#             delete_func = f"delete{base_name}"

#             self.generated_routes.append(f"router.get('{express_path}', {get_one_func});")
#             self.generated_routes.append(f"router.put('{express_path}', {update_func});")
#             self.generated_routes.append(f"router.delete('{express_path}', {delete_func});")
#             self.controller_map[controller_file].extend([get_one_func, update_func, delete_func])
#         else:
#             get_all_func = f"get{base_name}s"
#             create_func = f"create{base_name}"

#             self.generated_routes.append(f"router.get('{express_path}', {get_all_func});")
#             self.generated_routes.append(f"router.post('{express_path}', {create_func});")
#             self.controller_map[controller_file].extend([get_all_func, create_func])

# def convert_urls_with_ast(urls_path, views_path, output_path):
#     print("🧠 Analyzing views.py with AST to map views to models...")
#     try:
#         with open(views_path, 'r') as f:
#             views_content = f.read()
#         views_tree = ast.parse(views_content)
#         view_parser = ViewParser()
#         view_parser.visit(views_tree)
#         view_to_model_map = view_parser.view_to_model
#         print(f"✅ Found model mappings: {view_to_model_map}")
#     except FileNotFoundError:
#         print(f"❌ ERROR: Views file not found at '{views_path}'")
#         return

#     print(f"🚀 Converting '{urls_path}' using model mappings...")
#     try:
#         with open(urls_path, 'r') as f:
#             urls_content = f.read()
#         urls_tree = ast.parse(urls_content)
#         url_parser = URLParser(view_to_model_map)
#         url_parser.visit(urls_tree)
#     except FileNotFoundError:
#         print(f"❌ ERROR: URLs file not found at '{urls_path}'")
#         return

#     output_dir = os.path.dirname(output_path)
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     with open(output_path, 'w') as f:
#         f.write("const express = require('express');\nconst router = express.Router();\n\n")
#         f.write("// Import Controller Functions (grouped by model)\n")
#         for controller, functions in sorted(url_parser.controller_map.items()):
#             unique_functions = sorted(list(set(functions)))
#             f.write(f"const {{\n  {',\n  '.join(unique_functions)}\n}} = require('../controllers/{controller}');\n\n")

#         f.write("// --- API Routes ---\n")
#         for route in sorted(url_parser.generated_routes):
#             f.write(f"{route}\n")
#         f.write("\nmodule.exports = router;\n")

#     print(f"✅ Successfully created '{output_path}'")

# if __name__ == "__main__":
#     if len(sys.argv) < 3:
#         print("Usage: python urls_converter.py <urls.py path> <views.py path> [<output.js path>]")
#         sys.exit(1)

#     input_urls = sys.argv[1]
#     input_views = sys.argv[2]
#     output_js = sys.argv[3] if len(sys.argv) > 3 else "media/output_project/apiRoutes.js"

#     convert_urls_with_ast(input_urls, input_views, output_js)


import ast
import re
import os
import sys
from collections import defaultdict

class ViewParser(ast.NodeVisitor):
    def __init__(self):
        self.view_to_model = {}
        self.current_class = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        for item in node.body:
            if isinstance(item, ast.Assign):
                if len(item.targets) == 1 and isinstance(item.targets[0], ast.Name) and item.targets[0].id == 'model':
                    if isinstance(item.value, ast.Name):
                        model_name = item.value.id
                        self.view_to_model[self.current_class] = model_name
        self.current_class = None


class URLParser(ast.NodeVisitor):
    def __init__(self, view_to_model_map):
        self.view_to_model = view_to_model_map
        self.generated_routes = []
        self.controller_map = defaultdict(list)

    def visit_Assign(self, node):
        if len(node.targets) == 1 and getattr(node.targets[0], 'id', None) == 'urlpatterns':
            if isinstance(node.value, ast.List):
                for call_node in node.value.elts:
                    if isinstance(call_node, ast.Call) and getattr(call_node.func, 'id', '') == 'path':
                        self._process_path_call(call_node)

    def _process_path_call(self, node):
        if not node.args:
            return

        # Extract route path
        django_path = getattr(node.args[0], 'value', None)
        if not django_path:
            return

        express_path = f"/{re.sub(r'<[^:]+:(\w+)>', r':\1', django_path)}"

        # Try to extract view name
        view_node = node.args[1]
        view_name = None

        # Case: views.MyView.as_view()
        if isinstance(view_node, ast.Call) and isinstance(view_node.func, ast.Attribute) and view_node.func.attr == 'as_view':
            if isinstance(view_node.func.value, ast.Attribute):
                view_name = view_node.func.value.attr
            elif isinstance(view_node.func.value, ast.Name):
                view_name = view_node.func.value.id

        # Case: views.function_view
        elif isinstance(view_node, ast.Attribute):
            view_name = view_node.attr

        # Case: path(..., my_function_view)
        elif isinstance(view_node, ast.Name):
            view_name = view_node.id

        if not view_name:
            return

        model_name = self.view_to_model.get(view_name)
        controller_file = f"{model_name.lower()}Controller" if model_name else "genericController"

        is_detail_route = bool(re.search(r':\w+/?$', express_path))
        base_name = view_name.replace('View', '').replace('Detail', '').replace('List', '').replace('_view', '')

        if is_detail_route:
            get_one_func = f"get{base_name}"
            update_func = f"update{base_name}"
            delete_func = f"delete{base_name}"

            self.generated_routes.append(f"router.get('{express_path}', {get_one_func});")
            self.generated_routes.append(f"router.put('{express_path}', {update_func});")
            self.generated_routes.append(f"router.delete('{express_path}', {delete_func});")
            self.controller_map[controller_file].extend([get_one_func, update_func, delete_func])
        else:
            get_all_func = f"get{base_name}s"
            create_func = f"create{base_name}"

            self.generated_routes.append(f"router.get('{express_path}', {get_all_func});")
            self.generated_routes.append(f"router.post('{express_path}', {create_func});")
            self.controller_map[controller_file].extend([get_all_func, create_func])


def convert_urls_with_ast(urls_path, views_path, output_path):
    print("🧠 Analyzing views.py with AST to map views to models...")

    try:
        with open(views_path, 'r') as f:
            views_tree = ast.parse(f.read())
        view_parser = ViewParser()
        view_parser.visit(views_tree)
        view_to_model_map = view_parser.view_to_model
        print(f"✅ Found model mappings: {view_to_model_map}")
    except FileNotFoundError:
        print(f"❌ ERROR: Views file not found at '{views_path}'")
        return

    print(f"🚀 Converting '{urls_path}' using model mappings...")

    try:
        with open(urls_path, 'r') as f:
            urls_tree = ast.parse(f.read())
        url_parser = URLParser(view_to_model_map)
        url_parser.visit(urls_tree)
    except FileNotFoundError:
        print(f"❌ ERROR: URLs file not found at '{urls_path}'")
        return

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write final JS router file
    with open(output_path, 'w') as f:
        f.write("const express = require('express');\nconst router = express.Router();\n\n")
        f.write("// Import Controller Functions (grouped by model)\n")

        for controller, functions in sorted(url_parser.controller_map.items()):
            unique_functions = sorted(list(set(functions)))
            if unique_functions:
                f.write(f"const {{\n  {',\n  '.join(unique_functions)}\n}} = require('../controllers/{controller}');\n\n")

        f.write("// --- API Routes ---\n")
        for route in sorted(url_parser.generated_routes):
            f.write(f"{route}\n")

        f.write("\nmodule.exports = router;\n")

    print(f"✅ Successfully created '{output_path}'")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python urls_converter.py <urls.py path> <views.py path> [<output.js path>]")
        sys.exit(1)

    input_urls = sys.argv[1]
    input_views = sys.argv[2]
    output_js = sys.argv[3] if len(sys.argv) > 3 else "media/output_project/apiRoutes.js"

    convert_urls_with_ast(input_urls, input_views, output_js)

