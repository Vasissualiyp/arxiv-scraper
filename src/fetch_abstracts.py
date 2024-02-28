import requests
from bs4 import BeautifulSoup
import json
import os
import re
import csv
from datetime import datetime
from configuration import Config

# Obtain data from the webpage
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

# Reformatting latex
def correct_math_format(abstract):

    # Escape % signs not already escaped
    abstract = re.sub(r'(?<!\\)%', r'\%', abstract)
    
    """
    # Find all instances of math expressions with ^ or _
    # that are not already inside $...$ and enclose them in $...$
    # This regex looks for patterns outside $ signs
    patterns = [
        (r'(?<!\$)([\^_][^\s]+)(?!\$)', r'$\1$'),  # Enclose ^ or _ followed by non-space characters
        (r'(?<!\$)([\^_]\{[^\}]+\})(?!\$)', r'$\1$')  # Enclose ^ or _ followed by {..}
    ]

    for pattern, replacement in patterns:
        abstract = re.sub(pattern, replacement, abstract)
    """
    # For now, haven't created a function that will correct the math as needed - the function above will only make everything worse
    # So currently only take care of usage of % sign that forces to comment the latex line, if used without \

    return abstract

def latex_begin_end_strings():
    begin_string = r"""
\documentclass[14pt]{extarticle}

\usepackage[utf8]{inputenc} % Allows input to be in utf8
\usepackage{amsmath}        % For mathematical symbols
\usepackage{amsfonts}       % For mathematical fonts
\usepackage{amssymb}        % For mathematical symbols
\usepackage{geometry}       % For setting margins

% Set the page margins to 1 inch all around:
\geometry{letterpaper, portrait, margin=0.5in}

\begin{document}
    """

    end_string = r"""
\end{document}
    """
    return begin_string, end_string

def combine_into_latex_string(related_papers_content, papers_info):
    with open(related_papers_content, 'w') as tex_file:
        for title, arxiv_number, authors, abstract in papers_info:
            title_line = f"\\section{{{title}}}\n"
            link_line = f"\\url{{https://arxiv.org/pdf/{arxiv_number}.pdf}}\n\n{{arXiv:{arxiv_number}}}\n\n"
            authors_line = f"\\textbf{{{authors}}}\n\n"
            abstract_line = f"{abstract}\n\n"
            tex_file.write(title_line + link_line + authors_line + abstract_line)

# Create readible latex
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

def create_tex_main(config):
    # Load the related papers from the JSON file
    template_tex = config.TemplateTex 
    related_papers_json = config.RelatedPapersJson 
    related_papers_tex = config.OutputTexFile 
    related_papers_content = config.RelatedPapersContent 
    speech_tex_file = config.SpeechTexFile
    separate_papers_folder = config.SeparatePapersFolder

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
    combine_into_latex_string(related_papers_content, papers_info)

    # Write to a LaTeX file for speech generation
    combine_into_speech_string(speech_tex_file, papers_info)

    # Example usage:
    create_final_latex_document(template_tex, related_papers_content, related_papers_tex)

# Speech latex part
def create_speech_string_for_single_paper(tex_file, index, total_papers, title, arxiv_number, authors, abstract):

    """
    This function creates a string for the AI to read from. It is not intended to be human-readible.
    """

    # Include the number of the paper
    number_of_entry = f"Paper Number {index} out of {total_papers}\n"
    # Create a tex file entry with all necessary info
    title_line = f"Title: {title}\n"
    authors_line = f"Authors: {authors}\n"
    abstract_line = f"Abstract: {abstract}\n\n"
    tex_file.write(number_of_entry + title_line + authors_line + abstract_line)

def create_tex_string_for_single_paper(tex_file, index, total_papers, title, arxiv_number, authors, abstract):

    """
    This function creates a string for the AI to read from. It is not intended to be human-readible.
    """

    # Include the number of the paper
    number_of_entry = f"Paper Number {index} out of {total_papers}\n"

    # Create a tex file entry with all necessary info
    title_line = f"\\section*{{{title}}}\n\n"
    arxiv_line = f"\\textbf{{Arxiv number}}: \\textbf{{{arxiv_number}}}\n\n"
    authors_line = f"\\textbf{{Authors}}: \\textbf{{{authors}}}\n\n"
    abstract_line = f"\\textbf{{Abstract}}: {abstract}\n\n"
    tex_file.write(number_of_entry + title_line + arxiv_line +  authors_line + abstract_line)

def combine_into_speech_string(speech_tex_file, papers_info):
    begin_string = f"\\begin{{document}}\n\n"
    end_string = f"\\end{{document}}\n\n"

    with open(speech_tex_file, 'w') as tex_file:
        total_papers = len(papers_info)
        tex_file.write(begin_string)
        for index, (title, arxiv_number, authors, abstract) in enumerate(papers_info, start=1):
            create_speech_string_for_single_paper(tex_file, index, total_papers, title, arxiv_number, authors, abstract)
        tex_file.write(end_string)

def create_separate_tex_files_for_each_paper(separate_papers_folder, papers_info):
    """
    This function creates a tex file that the voiceover will be taking info from
    """
    begin_string, end_string = latex_begin_end_strings()
    total_papers = len(papers_info)
    for index, (title, arxiv_number, authors, abstract) in enumerate(papers_info, start=1):
        # Create a voiceover file (not intended to be human-readible)
        tex_file_name = str(index) + '_speech.tex'
        speech_tex_file = os.path.join(separate_papers_folder, tex_file_name)
        with open(speech_tex_file, 'w') as tex_file:
            tex_file.write(begin_string)
            create_speech_string_for_single_paper(tex_file, index, total_papers, title, arxiv_number, authors, abstract)
            tex_file.write(end_string)
        # Create a readible file (will be shown in the video)
        tex_file_name = str(index) + '_read.tex'
        speech_tex_file = os.path.join(separate_papers_folder, tex_file_name)
        with open(speech_tex_file, 'w') as tex_file:
            tex_file.write(begin_string)
            create_tex_string_for_single_paper(tex_file, index, total_papers, title, arxiv_number, authors, abstract)
            tex_file.write(end_string)

def create_all_speech_files_main(config):
    # Load the related papers from the JSON file
    template_tex = config.TemplateTex 
    related_papers_json = config.RelatedPapersJson 
    related_papers_tex = config.OutputTexFile 
    related_papers_content = config.RelatedPapersContent 
    speech_tex_file = config.SpeechTexFile
    separate_papers_folder = config.SeparatePapersFolder

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

    # Write to a speech and read LaTeX files
    create_separate_tex_files_for_each_paper(separate_papers_folder, papers_info)

    # Write to a LaTeX file for speech generation
    #combine_into_speech_string(speech_tex_file, papers_info)

    # Example usage:
    #create_final_latex_document(template_tex, related_papers_content, related_papers_tex)

# Functions for working outside of latex framework
def get_arxiv_numbers_for_date(config, date):

    csv_location = config.ArchiveFile
    arxiv_details_dict = {}  # Use a dictionary instead of a list
    with open(csv_location, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Date'] == date:
                # Directly insert into the dictionary
                arxiv_details_dict[row['Arxiv Number']] = row['Title']
    return arxiv_details_dict

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


if __name__ == "__main__":
    create_tex_main()
