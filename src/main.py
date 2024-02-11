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
from create_movie import create_video_files
from create_movie import combine_videos

def main(date = "current", combined_file_flag = False):
    """
    Main function to fetch, categorize, and process arXiv papers.

    This function performs a series of operations to scrape new submissions from arXiv,
    categorize them using AI, and optionally combine them into a single TeX document and/or
    generate text-to-speech summaries. The behavior of the function changes based on the
    input parameters.

    Parameters:
    - date (str): Specifies the date for which to fetch arXiv papers. If 'current', the function
      scrapes new submissions from arXiv. For any other date, it retrieves papers published on that
      specific date. The date format should match the expected format by `get_arxiv_numbers_for_date`.
    - combined_file_flag (bool): If True, the function creates a combined TeX file for all relevant
      papers and a single text-to-speech summary. If False, it generates individual speech and TeX files
      for each paper.

    Operations:
    1. Extracts configuration settings from a specified INI file.
    2. Based on the 'date' parameter, either scrapes new submissions from arXiv or fetches papers
       for a specific date.
    3. Categorizes papers using AI (assumed to filter relevant papers based on some criteria).
    4. Dumps the metadata of relevant papers into a JSON file for later processing.
    5. Depending on the 'combined_file_flag', either creates a combined TeX document and a single
       text-to-speech summary or generates individual files for each categorized paper.

    Side Effects:
    - Writes to files (CSV, JSON, TeX) in predefined directories.
    - Potentially makes network requests to arXiv and any used text-to-speech service.
    - Prints the response or outcome of various operations to stdout.

    Returns:
    None
    """
    # Extract config
    config = extract_configuration('config/config.ini')

    if date == "current":
        # Scrape arxiv for recent papers
        papers = scrape_arxiv_new_submissions(config.ArxivURL)
        #archived_list_filename = 'workdir/archive.csv'
        #write_tuples_to_csv(papers, config)
        
        # Categorize recent papers with ChatGPT
        related_papers = ai_categorization_main(papers, config)
        # The function above will also add the discovered arxiv pages to the csv file

    else:
        related_papers = get_arxiv_numbers_for_date(config, date)

    # Now, put the papers to the json file, which will be later used to create the tex file
    dump_papers_to_json(related_papers, config)
    
    if combined_file_flag: 
        # Create a tex file with all relevant papers
        create_tex_main(config)
        
        # Create text-to-speech summary of the papers
        tts_main(config)
    else:
        # Create a tex files with all relevant papers
        create_all_speech_files_main(config)
        
        # Create speech and tex files
        tts_with_video_main(config)

if __name__ == '__main__':
    main(date = 'current', combined_file_flag = False)

