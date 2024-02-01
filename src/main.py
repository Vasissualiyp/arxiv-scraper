from categorize_papers import ai_categorization_main
from configuration import extract_configuration
from fetch_abstracts import create_tex_main
from fetch_abstracts import write_tuples_to_csv
from scrape_pages import scrape_arxiv_new_submissions
from scrape_pages import scrape_arxiv_abstract
from doc_to_speech import tts_main

# Extract config
config = extract_configuration('config/config.ini')

# Scrape arxiv for recent papers
papers = scrape_arxiv_new_submissions(config.ArxivURL)
archived_list_filename = 'workdir/archive.csv'
#write_tuples_to_csv(papers, config)

# Categorize recent papers with ChatGPT
ai_categorization_main(papers, config)
# The function above will also add the discovered arxiv pages to the csv file

# Create a tex file with all relevant papers
create_tex_main(config)

# Create text-to-speech summary of the papers
tts_main(config)
