import openai
from configparser import ConfigParser
import os

print(os.getcwd())
config_file = ConfigParser()
config_file.read("config.ini")
print(config_file["OPENAI"]["key"])
print(type(config_file["OPENAI"]["key"]))
print(config_file.sections())
openai.api_key = config_file["OPENAI"]["key"]

def generate_prompt(text, max_tokens):
    text = openai.Completion.create(
      model="text-davinci-003",
      prompt=text,
      max_tokens=max_tokens,
      temperature=0
    )
    return text["choices"][0]["text"]

def generate_image(input, num_images=1):
    images = openai.Image.create(
    prompt=input,
    #The number of images to generate. Must be between 1 and 10.
    n=num_images,
    #The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.
    size="512x512" )
    return images["data"]