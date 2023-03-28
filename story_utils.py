from pathlib import Path
import shutil
import os

from bs4 import BeautifulSoup as Soup
from git import Repo

def create_new_story(path_to_content, keywords, content, cover_image=Path("../title2.png")):
    cover_image = Path(cover_image)

    files = len(list(path_to_content.glob("*.html")))
    new_title = f"{files+1}.html"
    path_to_new_content = path_to_content/new_title

    shutil.copy(cover_image, path_to_content)
    if not os.path.exists(path_to_new_content):
        with open(path_to_new_content,"w") as f:
            f.write('<!DOCTYPE HTML> \n')
            f.write("<html>\n")
            f.write("<head>\n")
            f.write(f"<title> {keywords} </title>\n")
            f.write("</head>")
            f.write("<body>")
            f.write(f"<img src='{cover_image.name}' alt='Cover Image'> <br/>\n")
            f.write(f"<h1> {keywords} </h1>")
            f.write(content.replace("\n","<br/>\n"))
            f.write("</body>\n")
            f.write("</html>\n")
            print("Story Created")
            return path_to_new_content
    else:
        raise FileExistsError("File Already Exists, please check again ur name! ABORTING!")

def check_for_duplicate_links(path_to_new_content,links):
    urls = [str(link.get("href")) for link in links] #[1.html, 2.html,...]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    print(content_path)
    return content_path in urls

def write_to_index(PATH_TO_STORY, path_to_new_content):
    with open(PATH_TO_STORY/'index.html') as index:
        soup = Soup(index.read())
        
    links = soup.find_all('a')

    last_link = links[-1]
    
    if check_for_duplicate_links(path_to_new_content,links):
        raise ValueError("Link Already Exists!")

    link_to_new_story = soup.new_tag("a",href=Path(*path_to_new_content.parts[-2:]))
    link_to_new_story.string = path_to_new_content.name.split('.')[0]
    last_link.insert_after(link_to_new_story)

    with open(PATH_TO_STORY/'index.html','w') as f:
        f.write(str(soup.prettify(formatter='html')))

def update_story(path_to_story_repo, commit_message="Updated story"):
    repo = Repo(path_to_story_repo)
    repo.git.add(all=True)
    repo.index.commit(commit_message)
    origin = repo.remote(name='origin')
    origin.push()