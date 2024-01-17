import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_arxiv_abstract(arxiv_number):
    abstract_url = f'https://arxiv.org/abs/{arxiv_number}'
    response = requests.get(abstract_url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    abstract_block = soup.find('blockquote', class_='abstract mathjax')
    if abstract_block:
        return abstract_block.text.replace('Abstract:', '').strip()
    return None

if __name__ == "__main__":
    # Load the related papers from the JSON file
    with open('related_papers.json', 'r') as file:
        related_papers = json.load(file)

    # Fetch the abstracts
    papers_info = []
    for arxiv_number, title in related_papers.items():
        abstract = fetch_arxiv_abstract(arxiv_number)
        if abstract:
            papers_info.append((title, arxiv_number, abstract))

    # Write to a LaTeX file
    with open('related_papers.tex', 'w') as tex_file:
        for title, arxiv_number, abstract in papers_info:
            title_line = f"\\section{{{title}}}\n"
            link_line = f"\\href{{https://arxiv.org/pdf/{arxiv_number}.pdf}}{{arXiv:{arxiv_number}}}\n\n"
            abstract_line = f"{abstract}\n\n"
            tex_file.write(title_line + link_line + abstract_line)

