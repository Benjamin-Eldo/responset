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

def query_model(model_name, files):
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

    prompt_base = read_file('prompt.txt')
    prompt = f"{prompt_base.replace('<code>', html+css)}"
    response = generate(model_name, prompt)
    print(response['response'])
    return response['response'], html, css

def save_progress(dataset, model_name, output_path):
    # write the dataset to a file
    output_file = 'dataset_'+model_name.split(':')[0].replace('.', '-')+'_intermediate.json'
    print(f'-- Writing progress to file {output_file} --')
    filename = os.path.join(output_path, output_file)
    # if filename exists
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            updated = json.load(f)
        existing_entries = [d.get('website_id') for d in updated]
    else:
        updated = []
        existing_entries = []
    for data in dataset:
        if data.get('website_id') not in existing_entries:
            # only append if the website_id is not already in the file
            updated.append(data)
    with open(filename, 'w') as f:
        json.dump(updated, f, indent=4)

def save_dataset(dataset, model_name, output_path):
    output_file = 'dataset_'+model_name.split(':')[0].replace('.', '-')+'_full.json'
    print(f'-- Writing complete dataset to file {output_file} --')
    with open(os.path.join(output_path, output_file), 'w') as f:
        json.dump(dataset, f, indent=4)

def run_model_on_files(dataset_path):
    """Use CLI args to get model_name and run the model on all files in dataset/code/desktop/html and dataset/code/desktop/css.
    CLI Arguments, in order : Model name (MANDATORY), Dataset path, Starting file index, Output path

    Args:
        dataset_path (str): Path to the dataset folder, containing html and css folders. Assuming the html and css files have the same name.
    """
    model_name = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2]:
        dataset_path = sys.argv[2]
    
    path = os.listdir(os.path.join(dataset_path, 'html'))
    
    if len(sys.argv) > 3 and sys.argv[3]:
        # continue from a specific file index
        path = path[int(sys.argv[3]):]
        start_file_name = path[0].split('.')[0]
        print(f'-- Starting from file {start_file_name} --')

    output_path=os.getcwd()

    if len(sys.argv) > 4 and sys.argv[4]:
        output_path = sys.argv[4]
    try:
        model_name = model_name
        output_path = output_path

        dataset = []
        intermediate_dataset = []
        nb_websites = len(path)
        nb_processed = 0
        current_file_index = 0
        for file in path:
            # assuming the dataset_path includes 2 folders: html and css
            # each containing a file with the same name for the same website
            website_name = file.split('.')[0]
            html_path = os.path.join(dataset_path, 'html', website_name+'.html')
            css_path = os.path.join(dataset_path, 'css', website_name+'.css')
            print(f'-- Running model on {html_path}, {css_path} --')
            try:
                response, html_code, css_code = query_model(model_name, [html_path, css_path])
            except UnicodeDecodeError:
                print(f'Error reading file {html_path} or {css_path}. Skipping.')
                current_file_index += 1
                continue

            data = {
                "website_id": website_name, 
                "html_code": html_code, 
                "css_code": css_code, 
                "responsive_explanation": response
            }
            dataset.append(data)
            intermediate_dataset.append(data)
            nb_processed += 1
            current_file_index += 1
            print(f'-- {nb_processed}/{nb_websites} websites processed, current file index : {current_file_index} --')

            if nb_processed % 100 == 0 or current_file_index == nb_websites:
                # write the progress to a file
                save_progress(intermediate_dataset, model_name, output_path)
                intermediate_dataset = []

        # write the dataset to a file
        save_progress(dataset, model_name, output_path)
    except KeyboardInterrupt:
        print("Process interrupted by the user. Saving progress before exiting.")
        save_progress(intermediate_dataset, model_name, output_path)  # Save progress up to the last processed file
        print("Progress saved before exiting. ")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # on peut soit définir le path ici, soit le passer en argument à l'exécution du script en ligne de commande
    run_model_on_files('dataset/code/desktop')