from typing import List, Tuple
import json

def get_element_by_id(dataset, website_id):
    for element in dataset:
            if element['website_id'] == website_id: 
                return element
    return None

def get_website_ids(dataset_path : str) -> List[str] : 
    with open(dataset_path, 'r') as file:
        dataset = json.load(file)
        return [element['website_id'] for element in dataset]

def get_first_elements(code_tuple : List[Tuple[str, str, int]]) -> str:
    return [code_1 for code_1, _, _ in code_tuple]