from typing import List
import json
import re

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
            print()
            print("---", item['website_id'], "---")
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
    print(result)
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

if __name__ == '__main__':
    # res = parse_deepseek('dataset/dataset_deepseek-coder_intermediate.json', '1drv_com')
    res = parse_deepseek('dataset/dataset_deepseek-coder_intermediate.json')