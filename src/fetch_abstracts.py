import requests
from bs4 import BeautifulSoup
import json
import os
import re
import csv
from datetime import datetime
from configuration import Config

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

def fetch_arxiv_authors(arxiv_number):
    authors_url = f'https://arxiv.org/abs/{arxiv_number}'
    response = requests.get(authors_url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    # Depending on the exact structure of the page, the class name might change
    authors_block = soup.find('div', class_='authors')

    if not authors_block:
        return None

    # Extracting just the text, stripping and splitting by newline to handle multiple authors
    authors_list = [author.get_text().strip() for author in authors_block.find_all('a')]
    
    if len(authors_list) > 4:
        return f"{authors_list[0]} et al."
    else:
        return ', '.join(authors_list)

def correct_math_format(abstract):
    # Escape % signs not already escaped
    abstract = re.sub(r'(?<!\\)%', r'\%', abstract)
    
    # Find all instances of math expressions with ^ or _
    # that are not already inside $...$ and enclose them in $...$
    # This regex looks for patterns outside $ signs
    patterns = [
        (r'(?<!\$)([\^_][^\s]+)(?!\$)', r'$\1$'),  # Enclose ^ or _ followed by non-space characters
        (r'(?<!\$)([\^_]\{[^\}]+\})(?!\$)', r'$\1$')  # Enclose ^ or _ followed by {..}
    ]

    for pattern, replacement in patterns:
        abstract = re.sub(pattern, replacement, abstract)

    return abstract

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

def write_tuples_to_csv(papers, config):
    # Get today's date in the desired format
    filename = config.ArchiveFile 
    today_date = datetime.today().strftime('%Y-%m-%d')
    
    # Check if the file exists
    if not os.path.exists(filename):
        # Open the file in write mode to create it and write the header
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Date', 'Arxiv Number', 'Title'])

    # Open the CSV file in append mode
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Iterate over the list of tuples
        for paper in papers:
            # Append the current date and the tuple elements to the CSV file
            csv_writer.writerow([today_date] + list(paper))

def combine_into_into_latex_string(related_papers_content, papers_info):
    with open(related_papers_content, 'w') as tex_file:
        for title, arxiv_number, authors, abstract in papers_info:
            title_line = f"\\section{{{title}}}\n"
            link_line = f"\\url{{https://arxiv.org/pdf/{arxiv_number}.pdf}}\n\n{{arXiv:{arxiv_number}}}\n\n"
            authors_line = f"\\textbf{{{authors}}}\n\n"
            abstract_line = f"{abstract}\n\n"
            tex_file.write(title_line + link_line + authors_line + abstract_line)

def combine_into_into_speech_string(speech_tex_file, papers_info):
    with open(speech_tex_file, 'w') as tex_file:
        total_papers = len(papers_info)
        for index, (title, arxiv_number, authors, abstract) in enumerate(papers_info, start=1):
            # Include the number of the paper
            number_of_entry = f"Paper Number {index} out of {total_papers}\n"

            # Create a tex file entry with all necessary info
            title_line = f"Title: {title}\n"
            authors_line = f"Authors: {authors}\n"
            abstract_line = f"Abstract: {abstract}\n\n"
            tex_file.write(number_of_entry + title_line + authors_line + abstract_line)

def create_tex_main(config):
    # Load the related papers from the JSON file
    template_tex = config.TemplateTex 
    related_papers_json = config.RelatedPapersJson 
    related_papers_tex = config.OutputTexFile 
    related_papers_content = config.RelatedPapersContent 
    speech_tex_file = config.SpeechTexFile
    with open(related_papers_json, 'r') as file:
        related_papers = json.load(file)

    # Fetch the abstracts
    papers_info = []
    for arxiv_number, title in related_papers.items():
        abstract = fetch_arxiv_abstract(arxiv_number)
        abstract = correct_math_format(abstract) # This is needed to treat symbols like $, ^, _ as math expressions if they aren't already
        authors = fetch_arxiv_authors(arxiv_number)
        if abstract:
            papers_info.append((title, arxiv_number, authors, abstract))

    # Write to a LaTeX file
    combine_into_into_latex_string(related_papers_content, papers_info)

    # Write to a LaTeX file for speech generation
    combine_into_into_speech_string(speech_tex_file, papers_info)

    # Example usage:
    create_final_latex_document(template_tex, related_papers_content, related_papers_tex)


if __name__ == "__main__":
    create_tex_main()
