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

### Scraping
Once the libraries are installed , you should scrapped the HTML code using the jupyter notebook files ```webpage_scrapper.ipynb```. 

By executing ```get_website_html``` in the loop, this will save the codes in a ```output``` repository.

### Code cleaning


### Execution
To run the prompt on one models you can do: 

```sh
python run_models.py 'model_name'
```

It will used the HTML and CSS codes avaible at the path ```"dataset/code/desktop"``` you can change this path by editing ```run_model.py```

You can also run all yours models at once using :

```sh
python run_all_models.py 
```

You can edit this files to add the models you want to run.

### Comparing responses



## Result

The complete dataset is [available for download here](https://drive.google.com/file/d/1ESVi71Ff13zkkqznOiv5W_h7kZ0z4u3f/view?usp=sharing).
