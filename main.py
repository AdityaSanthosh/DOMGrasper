import re
import openai
from bs4 import BeautifulSoup

openai_key = "####"


def prompt_gpt(prompt, api_key):
    res = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        api_key=api_key
    )
    return res.choices[0].text.strip()


with open('page.html', 'r') as f:
    html = f.read()
pattern = r'<(textarea|input)\b[^>]*>'
modified_html = re.sub(pattern, '<ip>', html)

soup = BeautifulSoup(modified_html)

title_tag = soup.head.find('title')

title = title_tag.text if title_tag else None

if title:
    response = prompt_gpt(f"The title of the page is {title}", openai_key)

meta_description = soup.find('meta', attrs={"name": "description"})
description_content = meta_description['content'].strip() if meta_description else None

if description_content:
    response = prompt_gpt(f"The description of the page is {description_content}", openai_key)

og_meta_tags = soup.find_all('meta', attrs={"property": lambda x: x and x.startswith('og:')})
og_content_list = [tag.get('content') for tag in og_meta_tags]

nav_elements = soup.find_all('nav')
link_content = {}
for nav_element in nav_elements:
    aria_label = nav_element.get('aria-label')
    list_items = nav_element.find_all('li')
    li_text_list = [word.strip() for li in list_items for word in li.get_text().strip().split('\n') if word.strip()]
    if li_text_list:
        link_content[aria_label] = li_text_list

list_description = "The following content is present in this webpage: " + ", ".join(link_content)

response = prompt_gpt(list_description, openai_key)

headings = [heading.get_text(strip=True) for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

if headings:
    heading_description = "The following sections are present in this webpage: " + ", ".join(headings)

    response = prompt_gpt(heading_description, openai_key)

webpage_description = response.choices[0].text.strip()
