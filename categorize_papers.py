import os
from openai import OpenAI
import sys
import json

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

    # Extract the arxiv number of the last paper
    with open(last_paper_file, 'r') as file:
        last_paper_arxiv = file.readline().strip()
     
    for i in range(len(papers)):
        if papers[i][0] == last_paper_arxiv:
            return i
    return None

if __name__ == "__main__":
    #papers = [...]  # Your list of papers (arxiv_number, title)
    arxiv_url = 'https://arxiv.org/list/astro-ph/new'
    papers = scrape_arxiv_new_submissions(arxiv_url)

    topics_file = "topics.txt"
    last_paper_file = "last_paper.txt"
    last_paper_id = get_last_paper_id(papers, last_paper_file)
    papers=papers[:last_paper_id]
    print(papers)
    paper_titles = [title for _, title in papers]
    related_titles = categorize_papers(paper_titles, topics_file)
    
    # Get the arXiv numbers of the related papers
    related_arxiv_numbers = [arxiv for arxiv, title in papers if title in related_titles]
    related_papers = {arxiv: title for arxiv, title in papers if title in related_titles}

    # Write related papers to a JSON file to be used by the next script
    with open('related_papers.json', 'w') as file:
        #json.dump(related_arxiv_numbers, file)
        json.dump(related_papers, file)
