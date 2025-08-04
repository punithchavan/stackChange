import os
from collections import defaultdict
from .ast_utils import unparse_functions

def get_group_name(func_name):
    return func_name.split('_')[0] if '_' in func_name else 'misc'

def group_functions(func_nodes):
    grouped = defaultdict(list)
    for func in func_nodes:
        group = get_group_name(func.name)
        grouped[group].append(func)
    return grouped

def build_template(group_name, raw_code):
    return f"""// {group_name}.controller.js - Template

/*
Converted from Django views
*/

const {group_name}_controller = {{
    // {raw_code.replace(chr(10), chr(10) + '    // ')}
}};

module.exports = {group_name}_controller;
"""
