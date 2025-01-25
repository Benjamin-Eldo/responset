from typing import List, Tuple
import json
import re

def parse_stable_code(dataset_file : str, website_id : str) -> List[str] :

    with open(dataset_file, 'r') as file:
        dataset = json.load(file)
        for element in dataset:
            if element['website_id'] == website_id: 
                code_list : List[str] = re.findall(r'\`{3}([^\`]*)\`{3}', element['responsive_explanation'])
                for i in range(len(code_list)):
                    code_list[i] = code_list[i].replace('\n', ' ')
                    code_list[i] = code_list[i].replace('html', '')
                    code_list[i] = code_list[i].replace('css', '')
                    code_list[i] = re.sub(r'( +)', ' ', code_list[i])
                    code_list[i] = re.sub(r'^ ', '', code_list[i])
                    code_list[i] = re.sub(r' $', '', code_list[i])
                return code_list
    
    # return [code for code in dataset if dataset[code]['is_stable']]