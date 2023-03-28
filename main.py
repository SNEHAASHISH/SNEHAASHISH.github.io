from pathlib import Path 
import story_utils
import openai_utils

PATH_TO_STORY_REPO = Path("C:\\Users\\Lenovo\\Documents\\GitHub\\SNEHAASHISH.github.io\\.git")
PATH_TO_STORY = PATH_TO_STORY_REPO.parent
PATH_TO_CONTENT = PATH_TO_STORY/"content"
PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)

keywords = input("Enter the keywords: ")
print(openai_utils.create_prompt(keywords))
story_content = openai_utils.get_story_from_openai(keywords)

_, cover_image_save_path = openai_utils.get_blog_from_openai(keywords, "title2.png")
path_to_new_content = story_utils.create_new_story(PATH_TO_CONTENT, keywords, story_content, cover_image_save_path)
story_utils.write_to_index(PATH_TO_STORY, path_to_new_content)

story_utils.update_story(PATH_TO_STORY_REPO)