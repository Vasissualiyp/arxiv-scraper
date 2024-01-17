from categorize_papers import ai_categorization_main
from configuration import extract_configuration
from fetch_abstracts import create_tex_main
from scrape_pages import scrape_arxiv_new_submissions
from scrape_pages import scrape_arxiv_abstract

# Extract config
config = extract_configuration('config/config.ini')

# Scrape arxiv for recent papers
papers = scrape_arxiv_new_submissions(config.ArxivURL)

# Categorize recent papers with ChatGPT
ai_categorization_main(papers, config)

# Create a tex file with all relevant papers
create_tex_main(config)
