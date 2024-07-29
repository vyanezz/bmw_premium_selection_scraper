import re


def add_commas_to_json_list(json_string):
    pattern = re.compile(r'(\})(\s*\{)')
    corrected_json_string = pattern.sub(r'\1,\2', json_string)
    return corrected_json_string
