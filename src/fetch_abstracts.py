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
def create_final_latex_document(template_file, papers_file, output_file):
    """
    Combines a LaTeX template file with a file containing LaTeX content for papers,
    and appends an end document tag, saving the result to an output file.

    :param template_file: The file path to the LaTeX template.
    :param papers_file: The file path to the LaTeX content for papers.
    :param output_file: The file path where the final LaTeX document should be saved.
    """
    try:
        # Read the template file content
        with open(template_file, 'r') as file:
            template_content = file.read()

        # Read the papers file content
        with open(papers_file, 'r') as file:
            papers_content = file.read()

        # Combine the template content with papers content and end document tag
        final_content = template_content + '\n' + papers_content + '\n\\end{document}'

        # Save the combined content to the output file
        with open(output_file, 'w') as file:
            file.write(final_content)

        print(f"The final document has been saved to {output_file}")

    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")



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
    with open('related_papers_content.tex', 'w') as tex_file:
        for title, arxiv_number, abstract in papers_info:
            title_line = f"\\section{{{title}}}\n"
            link_line = f"\\url{{https://arxiv.org/pdf/{arxiv_number}.pdf}}{{arXiv:{arxiv_number}}}\n\n"
            abstract_line = f"{abstract}\n\n"
            tex_file.write(title_line + link_line + abstract_line)

    # Example usage:
    create_final_latex_document('template.tex', 'related_papers_content.tex', 'related_papers.tex')

