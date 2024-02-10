from categorize_papers import ai_categorization_main
from categorize_papers import dump_papers_to_json
from configuration import extract_configuration
from fetch_abstracts import create_tex_main
from fetch_abstracts import write_tuples_to_csv
from fetch_abstracts import get_arxiv_numbers_for_date
from fetch_abstracts import create_all_speech_files_main
from scrape_pages import scrape_arxiv_new_submissions
from scrape_pages import scrape_arxiv_abstract
from doc_to_speech import tts_main
from doc_to_speech import tts_with_video_main

def csv_main():
    # Extract config
    config = extract_configuration('config/config.ini')

    date = "2024-02-06"

    related_papers = get_arxiv_numbers_for_date(config, date)

    # Now, put the papers to the json file, which will be later used to create the tex file
    dump_papers_to_json(related_papers, config)
    
    # Create a tex files with all relevant papers
    create_all_speech_files_main(config)
    
    # Create speech and tex files
    tts_with_video_main(config)

    

def main():
    # Extract config
    config = extract_configuration('config/config.ini')
    
    # Scrape arxiv for recent papers
    papers = scrape_arxiv_new_submissions(config.ArxivURL)
    #archived_list_filename = 'workdir/archive.csv'
    #write_tuples_to_csv(papers, config)
    
    # Categorize recent papers with ChatGPT
    related_papers = ai_categorization_main(papers, config)
    # The function above will also add the discovered arxiv pages to the csv file

    # Now, put the papers to the json file, which will be later used to create the tex file
    dump_papers_to_json(related_papers, config)
    
    # Create a tex file with all relevant papers
    create_tex_main(config)
    
    # Create text-to-speech summary of the papers
    tts_main(config)

if __name__ == '__main__':
    #main()
    csv_main()

