import requests
from bs4 import BeautifulSoup

def fetch_markdown_from_url(url: str): #returns str
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch: {url}")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

def load_docs_from_urls(urls):
    docs = []
    for url in urls:
        print(f"Fetching: {url}")
        text = fetch_markdown_from_url(url)
        docs.append(text)
    return docs

