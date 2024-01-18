import os
from openai import OpenAI
import sys
import json
import sys

from configuration import Config
from scrape_pages import scrape_arxiv_new_submissions
from scrape_pages import scrape_arxiv_abstract

# Initialize the OpenAI API client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model_engine = "gpt-3.5-turbo"


def categorize_papers(paper_titles, topics_file):
    # Read the topics
    try:
        with open(topics_file, 'r') as file:
            topics = file.read()
    except FileNotFoundError:
        print(f"Topics file {topics_file} not found.")
        return

    related_papers = []

    for title in paper_titles:
        print(f"Using ChatGPT to categorize the paper title: '{title}'...")

        # Generate content for the categorization
        response = client.chat.completions.create(
            model=model_engine,
            messages=[
                {"role": "user", "content": f"""
                Given the list of topics:
                {topics}

                Please indicate if the following paper title is related to any of the topics listed above:
                Paper Title: {title}

                Respond with 'Yes' if it is related, otherwise respond with 'No'.
                """}
            ]
        )

        try:
            is_related = response.choices[0].message.content.strip().lower()
            if is_related == 'yes':
                related_papers.append(title)
        except KeyError as e:
            print(f"KeyError: {e}")
            print("Could not find the required key in the response.")
            return []

    return related_papers

def get_last_paper_id(papers, last_paper_file):

    if os.path.exists(last_paper_file):
        # Extract the arxiv number of the last paper
        with open(last_paper_file, 'r') as file:
            last_paper_arxiv = file.readline().strip()
         
        for i in range(len(papers)):
            if papers[i][0] == last_paper_arxiv:
                return i
        return None
    else:
        return len(papers)

def save_first_arxiv_number(papers, last_paper_file):
    """
    Save the first arXiv number from the list of papers to a file.

    :param papers: List of tuples containing (arxiv_number, title)
    :param last_paper_file: File path to save the first arXiv number
    """
    if papers:  # Check if the papers list is not empty
        first_arxiv_number = papers[0][0]  # Get the first arXiv number
        with open(last_paper_file, 'w') as file:
            file.write(first_arxiv_number + '\n')  # Write the arXiv number to the file
        print(f"The first arXiv number has been saved to {last_paper_file}")
    else:
        print("The papers list is empty. No arXiv number was saved.")

def ai_categorization_main(papers, config):
    #papers = [...]  # Your list of papers (arxiv_number, title)
    topics_file = config.TopicsFile
    last_paper_file = config.LastPaperFile
    related_papers_json = config.RelatedPapersJson

    last_paper_id = get_last_paper_id(papers, last_paper_file)
    if last_paper_id == 0:
        print("The arxiv has already been successfully scraped up-to-date. Exiting...")
        sys.exit(0)
    papers=papers[:last_paper_id]
    print(papers)
    paper_titles = [title for _, title in papers]
    related_titles = categorize_papers(paper_titles, topics_file)
    save_first_arxiv_number(papers, last_paper_file)
    
    # Get the arXiv numbers of the related papers
    related_arxiv_numbers = [arxiv for arxiv, title in papers if title in related_titles]
    related_papers = {arxiv: title for arxiv, title in papers if title in related_titles}

    # Overwrite related papers to a JSON file to be used by the next script
    if os.path.exists(related_papers_json):
        os.remove(related_papers_json)
    with open(related_papers_json, 'w') as file:
        #json.dump(related_arxiv_numbers, file)
        json.dump(related_papers, file)

if __name__ == "__main__":
    ai_categorization_main()
