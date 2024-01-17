import os
from openai import OpenAI
import sys
from scrape_pages import scrape_arxiv_new_submissions
from scrape_pages import scrape_arxiv_abstract

# Initialize the OpenAI API client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# If the environment variable is not set, you can uncomment the following line and set the API key directly
# openai.api_key = "your-api-key-here"

model_engine = "gpt-4"

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

if __name__ == "__main__":
    # Assuming 'papers' is a list of tuples (arxiv_number, title)
    arxiv_url = 'https://arxiv.org/list/astro-ph/new'
    papers = scrape_arxiv_new_submissions(arxiv_url)

    n = int(sys.argv[1]) if len(sys.argv) > 1 else len(papers)
    topics_file = "topics.txt"  # Replace with your actual topics file path

    paper_titles = [title for _, title in papers[:n]]
    related_papers = categorize_papers(paper_titles, topics_file)

    print("Related papers:")
    for paper in related_papers:
        print(paper)
