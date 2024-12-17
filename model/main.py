# from ollama import chat
# from ollama import ChatResponse
# import streamlit as st


# # import base64
# # from PIL import Image

# # def preprocess_and_encode_image(image_path, output_size=(672, 672)):
# #     with Image.open(image_path) as img:
# #         img = img.convert("RGB")
# #         img = img.resize(output_size)
# #         img.save("processed_image.jpg")
# #     with open("processed_image.jpg", "rb") as img_file:
# #         return base64.b64encode(img_file.read()).decode("utf-8")
    
# # encoded_image = preprocess_and_encode_image("flower.jpg")

# response: ChatResponse = chat(model='llava:7b', messages=[
#   {
#     'role': 'user',
#     'content': 'What is write on this image?',
#     'images': ['images/test.png']
#   },
# ])

# print(response.message.content)

import gradio as gr
from gradio.data_classes import FileData
from ollama import chat, ChatResponse
import base64
from PIL import Image

history = []

def preprocess_and_encode_image(image_path, output_size=(672, 672)):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img = img.resize(output_size)
        img.save("processed_image.jpg")
    with open("processed_image.jpg", "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def response(input, _):
    message = input['text']
    image = input['files']
    print("This image ", image)

    if image:
        image = image[0]
        encoded_image = preprocess_and_encode_image(image)

        new_message = {
                'role': 'user',
                'content': message,
                'images': [encoded_image] 
        }
    else:
       new_message = {
                'role': 'user',
                'content': message
        }
    
    history.append(new_message)
    response: ChatResponse = chat(model='llava:7b', messages=history)
    history.append({
        'role': 'assistant',
        'content': response.message.content
    })
       
    return response.message.content
    
demo = gr.ChatInterface(
    fn=response,
    # additional_inputs=[
    #     gr.Image(type="filepath", label="Choose a image", scale=0.3),
    # ],
    autofocus=False,
    title='Web2code-M',
    description='Easily responsive code for your favorite web site',
    multimodal=True
)

if __name__ == "__main__":
    demo.launch()

    
