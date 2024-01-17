import requests
from bs4 import BeautifulSoup

def scrape_arxiv_new_submissions(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    papers = []

    for dd_tag in soup.find_all('dd'):
        title_tag = dd_tag.find('div', class_='list-title mathjax')
        title = title_tag.text.strip().replace('Title: ', '')

        dt_tag = dd_tag.find_previous_sibling('dt')
        arxiv_num = dt_tag.text.replace('[', '').replace(']', '').strip()
        # Extract the arXiv number which is usually in the format arXiv:XXXX.XXXXX
        arxiv_num = arxiv_num.split('arXiv:')[-1].split()[0]

        papers.append((arxiv_num, title))

    return papers

arxiv_url = 'https://arxiv.org/list/astro-ph/new'
papers = scrape_arxiv_new_submissions(arxiv_url)

# Output the first few papers to check
for paper in papers[:5]:
    print(f"Arxiv Number: {paper[0]}, Title: {paper[1]}")
