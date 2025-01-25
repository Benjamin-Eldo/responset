from typing import List, Tuple
import json
import re

def parse_stable_code(dataset_file : str, website_id : str) -> List[str] :

    with open(dataset_file, 'r') as file:
        dataset = json.load(file)
        for element in dataset:
            if element['website_id'] == website_id: 
                # print(element['responsive_explanation'])
                code_list : List[str] = []
                code_list.extend(parse_md_format(element['responsive_explanation']))
                # code_list.extend(parse_exclamation_format(element['responsive_explanation']))
                code_list = list(dict.fromkeys(code_list))
                code_list = clear_code(code_list)
                return code_list
    
    # return [code for code in dataset if dataset[code]['is_stable']]


def parse_md_format(llm_response : str) -> List[str] : 
    code_list : List[str] = re.findall(r'\`{3}([^\`]*)\`{3}', llm_response)
    code_list.extend(re.findall(r'\`([^\`]*)\`', llm_response))
    code_list = clear_code(code_list)
    return code_list


def parse_exclamation_format(llm_response : str) -> List[str] :
    llm_response = llm_response.strip()
    llm_response = llm_response.replace('\n', ' ')
    code_list : List[str] = llm_response.split('!')
    code_list = clear_code(code_list)
    return code_list

def clear_code(code_list : List[str]) -> List[str] : 
    for i in range(len(code_list)):
        code_list[i] = code_list[i].replace('\n', ' ')
        code_list[i] = code_list[i].replace('html', '')
        code_list[i] = code_list[i].replace('css', '')
        code_list[i] = code_list[i].replace('```', ' ')
        code_list[i] = re.sub(r'( +)', ' ', code_list[i])
        code_list[i] = re.sub(r'^ ', '', code_list[i])
        code_list[i] = re.sub(r' $', '', code_list[i])
    return code_list