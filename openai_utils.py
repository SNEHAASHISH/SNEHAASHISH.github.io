import os
import requests
import shutil

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def create_prompt(keywords):
    prompt = '''
    Generate a story from the following keywords: {}
    '''.format(keywords)
    return prompt

def get_story_from_openai(keywords):
    response = openai.Completion.create(engine="text-davinci-003",
                                            prompt=create_prompt(keywords),
                                            max_tokens=512,
                                            temperature=0.7)

    return response["choices"][0]["text"]

def dalle2_prompt(keywords):
    prompt = f"An oil painting showing '{keywords}'"
    return prompt

def save_image(image_url, file_name):
    image_res = requests.get(image_url, stream=True)
    if image_res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(image_res.raw, f)
    else:
        print("Error downloading image!")
    return image_res.status_code, file_name

def get_cover_image(keywords, save_path):
    response = openai.Image.create(
        prompt = dalle2_prompt(keywords),
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    status_code, file_name = save_image(image_url,save_path)
    return status_code, file_name