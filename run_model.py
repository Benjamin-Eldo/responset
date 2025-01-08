from ollama import generate
import os
import sys

def read_file(file):
    """Read the contents of a file

    Args:
        file (str): File path

    Returns:
        str: Contents of the file
    """
    with open(file, 'r') as f:
        return f.read()

def run_model(model_name, files):
    """Run the model after extracting the contents of given files

    Args:
        model_name (str): LLM model name (ollama convention)
        files (list[str]): List of file paths for the HTML and CSS files
    """
    for file in files:
        if file.endswith('.html'):
            html = read_file(file)
        elif file.endswith('.css'):
            css = read_file(file)
    prompt = (
        f"What makes this code responsive ? Be concise.\n"
        f"<HTMLCODE>{str().join(html.split()[:200])}</HTMLCODE>\n"
        f"<CSSCODE>{str().join(css.split()[:200])}</CSSCODE>"
    )
    response = generate(model_name, prompt)
    print(response['response'])


# 
def run_model_on_files(dataset_path):
    """Use CLI args to get model_name and run the model on all files in dataset/code/desktop/html and dataset/code/desktop/css

    Args:
        dataset_path (str): Path to the dataset folder, containing html and css folders. Assuming the html and css files have the same name.
    """
    # llama3.2:1b
    model_name = sys.argv[1]
    if sys.argv[2]:
        dataset_path = sys.argv[2]
    for file in os.listdir(os.path.join(dataset_path, 'html')):
        # assuming the dataset_path includes 2 folders: html and css
        # each containing a file with the same name for the same website
        website_name = file.split('.')[0]
        html_path = os.path.join(dataset_path, 'html', website_name+'.html')
        css_path = os.path.join(dataset_path, 'css', website_name+'.css')
        print(f'\n\t--- Running model on {html_path}, {css_path} ---\n')
        run_model(model_name, [html_path, css_path])

# haha c'est un dossier avec 2 dossiers: html et css et qui contient juste 2 exemples pour tester de mon côté
run_model_on_files('haha')