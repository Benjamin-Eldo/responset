from typing import List, Tuple
import json
import re

def parse_stable(dataset_file : str, website_id : str) -> List[str] :

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


def parse_gemma(dataset : str, website_id : str) -> list[str]:
    parsed_responsive_line = []
    with open(dataset, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    responsive = None

    for site in data:
        if site.get("website_id") == website_id:
            responsive = site.get('responsive_explanation')
    
    responsive_lines = responsive.split("\n")
    for line in responsive_lines:
        parsed_line = line.strip("! `").rsplit("`", 1)[0].strip()
        parsed_line = parsed_line.replace("'", " ")
        parsed_responsive_line.append(parsed_line)

    return parsed_responsive_line

def parse_qwen_coder(dataset : str, website_id : str) -> list[str]:
    parsed_responsive_line = []
    with open(dataset, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    responsive = None

    for site in data:
        if site.get("website_id") == website_id:
            responsive = site.get('responsive_explanation')

    responsive_lines = re.findall("(@media.*\s*)| (`*[\.\#][^!}]*[!};])| !([^!]+)!|\`{3}([^\`]*)\`{3}|<([^>]+)>|^!([^!\n]*)", responsive, re.MULTILINE)
    for line in responsive_lines:
        parsed_line = next((x for x in line if x), None)
        
        if parsed_line:
            parsed_line = parsed_line.strip('! `').strip()
            parsed_line = parsed_line.replace("\n", " ")
            parsed_responsive_line.append(parsed_line)

    return parsed_responsive_line

def parse_deepseek(dataset_file : str, website_id : str = None) -> List[str]:
    with open(dataset_file, 'r') as file:
        dataset = json.load(file)

    if website_id:
        llm_response = [item for item in dataset if item['website_id'] == website_id][0]['responsive_explanation']
        return parse_une_reponse_deepseek(llm_response)
    else:
        # si besoin de tester en batch
        responses = []
        for item in dataset[:20]:
            res = parse_une_reponse_deepseek(item['responsive_explanation'])
            responses.append(res)
        return responses

def parse_une_reponse_deepseek(llm_response:str) -> List[str]:
    tokens_to_remove = ['<｜begin▁of▁sentence｜>', '<｜end▁of▁sentence｜>']

    for token in tokens_to_remove:
        llm_response = llm_response.replace(token, '')

    result = []

    # enlève les commentaires
    css_comments = re.compile(r'(\/\*.*\*\/)')
    css_comment_matches = css_comments.findall(llm_response)
    for match in css_comment_matches:
        llm_response = llm_response.replace(match, '')

    html_comments = re.compile(r'(<!--.*?-->)')
    html_comment_matches = html_comments.findall(llm_response)
    for match in html_comment_matches:
        llm_response = llm_response.replace(match, '')

    # capture les meta tags
    meta_tags = re.compile(r'(<meta.*?>)')
    meta_matches = parse_a_pattern(llm_response, meta_tags, result)

    # capture les media queries
    media_queries = re.compile(r'(@media[^\`{}]*{[^\`]*?})')
    media_matches = parse_a_pattern(llm_response, media_queries, result)

    # capture les blocs de code Markdown
    code_blocks = re.compile(r'\`{3}\w*\n([^\`]*)\`{3}')
    code_blocks_matches = code_blocks.findall(llm_response)
    for match in code_blocks_matches:
        if '!' in match:
            submatches = match.split('!')
            for submatch in submatches:
                clean_and_append_match(submatch, result)
        else:
            clean_and_append_match(match, result)

    raw_css = re.compile(r'(.+?{.+?;[\\n\s]*})')
    parse_a_pattern(llm_response, raw_css, result)
    
    digits_w_bang = re.compile(r'\d+!\s*\'(.+?)\'')
    parse_a_pattern(llm_response, digits_w_bang, result)

    if len(code_blocks_matches) ==  0:
        anything_within_backticks = re.compile(r'`([^`]*)`')
        inline_code_matches = parse_a_pattern(llm_response, anything_within_backticks, result)
        
        if inline_code_matches == 0 and meta_matches == 0 and media_matches == 0:
            one_line = re.compile(r'([^\n]*)\n$')
            parse_a_pattern(llm_response, one_line, result)

    set_result = set(result)
    result = list(set_result)
    return result

def clean_and_append_match(match:str, result:List[str]):
    """Removes newlines and tabs and strips leading & trailing whitespaces from the match and appends it to the result list.

    Args:
        match (str): string to clean
        result (List[str]): list to append the cleaned string to
    """
    match = match.replace('\n', '')
    match = match.replace('\t', '')
    match = match.rstrip().lstrip()
    match = re.sub(r'( +)', ' ', match)
    if match:
        result.append(match)

def parse_a_pattern(llm_response:str, pattern:re.Pattern, result:List[str]):
    """Parses a pattern in the llm_response and appends the matches to the result list.

    Args:
        llm_response (str): string to parse from
        pattern (re.Pattern): pattern to search for
        result (List[str]): list to append the matches to

    Returns:
        int: number of matches found
    """
    matches = pattern.findall(llm_response)
    for match in matches:
        clean_and_append_match(match, result)
    return len(matches)