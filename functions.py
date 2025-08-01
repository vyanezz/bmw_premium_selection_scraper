import re
import json

def add_commas_to_json_list(json_string):
    pattern = re.compile(r'(\})(\s*\{)')
    corrected_json_string = pattern.sub(r'\1,\2', json_string)
    return corrected_json_string

def correct_json(soup):
    try:
        script_tag = soup.find('script', {'type': 'application/ld+json'}).string
        json_ok = add_commas_to_json_list(script_tag)
        json_data = json.loads(json_ok)
        return json_data['itemListElement']
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON: {e}')