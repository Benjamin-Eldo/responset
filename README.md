# Responset 

This project consists of producing a dataset highlighting, in webpage code, what makes it responsive. The dataset is created using webpage code scrapped from the 1000 most popular websites using the [Tranco Ranking](https://tranco-list.eu/list/KJ58W). Then, several LLM are used to extract the code that enables the responsiveness of the website.

This project was realized in an Theory and Practical Applications of Large Language Models class during second year of Master Degree in Artificial Intelligence at University Lyon 1 Claude Bernard.

## Project members
- [SEN Abdurrahman](https://github.com/senabIsShort)
- [DESBIAUX Arthur](https://github.com/adesbx)
- [VADUREL Benjamin](https://github.com/Benjamin-Eldo)

## Video

[Here](https://youtu.be/irc_KAe42Jc)  is a short demo video presenting the subject.

## Models used

- [Stable code](https://ollama.com/library/stable-code:3b)
- [Qwen2.5-code](https://ollama.com/library/qwen2.5-coder:3b)
- [Starcoder2](https://ollama.com/library/starcoder2:3b)
- [Gemma](https://ollama.com/library/gemma:7b)
- [Deepseek](https://ollama.com/library/deepseek-coder:6.7b)

Of course you can used any other models avaible on [ollama](https://ollama.com/)

## Installation

### Setup
Once you pulled this GIT repository, you have to get to the project's root and install the required libraries.

```sh
#In the project's root
pip install -r requirements.txt
```

## Running

The dataset generation follows steps described in this pipeline. 

![Pipeline](/img/Pipeline.png "Pipeline").

Each step must be completed before it passes to the next one. The pipeline contains 4 steps : Webpage scrapping, Cleaning up the webpage code, Querying the LLMs on the webpage code and Comparing responses.

### Scrapping
```sh
cd scrapping-cleaning
```

Once the libraries are installed, you should scrap the HTML code using the jupyter notebook files ```webpage_scrapper.ipynb```. 

By executing ```get_website_html``` in the loop, this will save the codes in a ```output``` repository.

### Code cleaning
```sh
cd scrapping-cleaning
```
To clean the code, you should use the jupyter notebook files ```dataset_code_cleaning.ipynb```.

It will modify the code at the path ```"dataset/code/desktop/html/"``` and save the new one at ```"dataset/code/desktop/html_clean/"```.

Of course you can adapt the path with your own.

### Execution
```sh
cd llm-querying
```

To run the prompt on one model you can do: 

```sh
python run_models.py 'model_name'
```

It will use the HTML and CSS codes available at the path ```"dataset/code/desktop"``` you can change this path by editing ```run_model.py```

You can also run all your models at once using:

```sh
python run_all_models.py 
```

You can edit this file to add the models you want to run.

If you want to use your own prompt, you can modify the ```prompt.txt``` files

### Comparing responses
Here is how the responses are compared.

![Tournament](/img/diag_tournament.png "Diag tournament").

```sh
cd tournament
```

Finally, to create the dataset by comparing the result of the LLMs you should use the jupyter notebook files ```tournament.ipynb```.

You can run all the files, if you have add your own LLM model don't forget to add the parse code for it in ```response_parsing.py``` and import it in the jupyter notebook. Then modify ```tournament_for_website``` to add your parser as you want.

## Result

The complete dataset is [available for download here](https://drive.google.com/file/d/1ESVi71Ff13zkkqznOiv5W_h7kZ0z4u3f/view?usp=sharing).
