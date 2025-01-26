from typing import List, Tuple
from rouge_score import rouge_scorer
import json
from utils import get_first_elements


def confront_dataset(code_list_1 : list, code_list_2 : list) -> List[Tuple[str, str, int]]:
    """
    This function receives two lists of strings, each one containing a set of code snippets.
    It returns a list of tuples, where each tuple contains two code snippets and the similarity score between them.
    """
    tuple_with_score = []
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)    

    for code_1 in code_list_1:
        for code_2 in code_list_2:
            scores = scorer.score(code_1, code_2)
            tuple_with_score.append((code_1, code_2, scores['rougeL'].fmeasure))
    return tuple_with_score

def filter_pairs(tuple_list : List[Tuple[str, str, int]], threshold : float = 0.7) -> List[Tuple[str, str, int]]:
    """
    This function receives a list of tuples, each one containing two code snippets and the similarity score between them.
    It returns a list of tuples, where each tuple contains two code snippets and the similarity score between them.
    """
    return [(code_1, code_2, score) for code_1, code_2, score in tuple_list if score >= threshold]

def round(code_list_1 : list, code_list_2 : list, threshold = 0.5) -> List[str]:
    """
    This function receives two lists of strings, each one containing a set of code snippets.
    It returns a list of strings, where each string contains a code snippet from the first list and a code snippet from the second list.
    """
    if len(code_list_1) == 0: 
        return code_list_2
    
    if len(code_list_2) == 0:
        return code_list_1

    tuple_list = confront_dataset(code_list_1, code_list_2)
    filtered_list = filter_pairs(tuple_list, threshold)
    return list(dict.fromkeys(get_first_elements(filtered_list)))