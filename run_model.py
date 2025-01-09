from ollama import generate
import os
import sys
import json

def read_file(file):
    """Read the contents of a file

    Args:
        file (str): File path

    Returns:
        str: Contents of the file
    """
    with open(file, 'r') as f:
        return f.read()

def query_model(model_name, files, prompt_base):
    """Query the model after extracting the contents of given files

    Args:
        model_name (str): LLM model name (ollama convention)
        files (list[str]): List of file paths for the HTML and CSS files

    Returns:
        str: Model response
    """
    for file in files:
        if file.endswith('.html'):
            html = read_file(file)
        elif file.endswith('.css'):
            css = read_file(file)
    prompt = (
        f"{prompt_base}\n"
        f"<HTMLCODE>{str().join(html.split()[:200])}</HTMLCODE>\n"
        f"<CSSCODE>{str().join(css.split()[:200])}</CSSCODE>"
    )
    response = generate(model_name, prompt)
    print(response['response'])
    return response['response']


# 
def run_model_on_files(dataset_path):
    """Use CLI args to get model_name and run the model on all files in dataset/code/desktop/html and dataset/code/desktop/css

    Args:
        dataset_path (str): Path to the dataset folder, containing html and css folders. Assuming the html and css files have the same name.
    """
    # llama3.2:1b
    model_name = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2]:
        dataset_path = sys.argv[2]

    prompt_base = 'What makes this code responsive ? Be concise.'
    dataset = []

    for file in os.listdir(os.path.join(dataset_path, 'html')):
        # assuming the dataset_path includes 2 folders: html and css
        # each containing a file with the same name for the same website
        website_name = file.split('.')[0]
        html_path = os.path.join(dataset_path, 'html', website_name+'.html')
        css_path = os.path.join(dataset_path, 'css', website_name+'.css')
        print(f'\n\t-- Running model on {html_path}, {css_path} --\n')
        response = query_model(model_name, [html_path, css_path], prompt_base)
        data = {
            "id": website_name, 
            "html": html_path, 
            "css": css_path, 
            "response": response
        }
        dataset.append(data)

    # write the dataset to a file
    with open(os.path.join(dataset_path, 'dataset.json'), 'w') as f:
        json.dump(dataset, f, indent=4)

if __name__ == '__main__':
    # on peut soit définir le path ici, soit le passer en argument à l'exécution du script en ligne de commande
    run_model_on_files('dataset/code/desktop')