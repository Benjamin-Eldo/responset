import run_model

if __name__ == '__main__':
    models = ['stable-code:3b', 'qwen2.5-coder:3b', 'starcoder2:3b', 'gemma:2b', 'deepseek-coder']
    for model in models:
        run_model.run_model_on_files('dataset/code/desktop', model)