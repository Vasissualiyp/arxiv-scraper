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


def scrape_arxiv_abstract(arxiv_number):
    """
    Given an arXiv number, this function scrapes the corresponding paper's abstract from arXiv.org.

    :param arxiv_number: The arXiv number of the paper as a string
    :return: The abstract of the paper as a string
    """
    # Construct the URL for the abstract page
    abstract_url = f'https://arxiv.org/abs/{arxiv_number}'

    # Send a GET request to the abstract page
    response = requests.get(abstract_url)

    # Check if the request was successful
    if response.status_code != 200:
        return f"Failed to retrieve the abstract page, status code: {response.status_code}"

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the abstract block
    abstract_block = soup.find('blockquote', class_='abstract mathjax')
    if abstract_block:
        # Clean the abstract text by removing the "Abstract" word and leading/trailing whitespaces
        abstract_text = abstract_block.text.replace('Abstract', '').strip()
        return abstract_text
    else:
        return "Abstract not found."


arxiv_url = 'https://arxiv.org/list/astro-ph/new'
papers = scrape_arxiv_new_submissions(arxiv_url)

# Output the first few papers to check
for paper in papers[:5]:
    print(f"Arxiv Number: {paper[0]}, Title: {paper[1]}")

# Example usage:
# Let's say the first element of the papers array has the arXiv number '2401.06841'
arxiv_number_of_first_paper = papers[0][0]  # Assuming 'papers' is the list of tuples (arxiv_number, title)
abstract = scrape_arxiv_abstract(arxiv_number_of_first_paper)
print(abstract)
