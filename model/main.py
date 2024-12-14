from ollama import chat
from ollama import ChatResponse

# import base64
# from PIL import Image

# def preprocess_and_encode_image(image_path, output_size=(672, 672)):
#     with Image.open(image_path) as img:
#         img = img.convert("RGB")
#         img = img.resize(output_size)
#         img.save("processed_image.jpg")
#     with open("processed_image.jpg", "rb") as img_file:
#         return base64.b64encode(img_file.read()).decode("utf-8")
    
# encoded_image = preprocess_and_encode_image("flower.jpg")

response: ChatResponse = chat(model='llava:7b', messages=[
  {
    'role': 'user',
    'content': 'What is write on this image?',
    'images': ['test.png']
  },
])
print(response.message.content)
