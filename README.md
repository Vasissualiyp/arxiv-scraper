# ArXiv Abstract Scraper and Compiler

This script is designed to efficiently gather abstracts of the latest arXiv papers, filtering them based on topics relevant to your specific field of interest. The relevance of papers is determined using the ChatGPT API. This tool compiles the selected abstracts into a single LaTeX document, streamlining your research process by providing you with information that is directly pertinent to your area of study.

## Installation

### Prerequisites
- Python installed with pip
- A valid OpenAI API key for accessing the ChatGPT API

### Steps
1. Obtain your OpenAI API key. Instructions can be found [here](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/).
2. Execute the setup script by running:
`setup.sh`
This script will guide you through the necessary steps, including entering your OpenAI API key, creating a Python virtual environment, and installing all required Python libraries.

## Execution

To run the script, execute the following command:
`run.sh`
This command initiates the process of scraping arXiv for paper titles, using ChatGPT to identify papers relevant to your specified topics, extracting their abstracts, and compiling them into a LaTeX document. The document is then saved in the `workdir` directory, after which it is transferred to a user-specified folder.

## Configuration

Customize your experience by modifying the `config.ini` file located in the `config` folder. Important details:
- `TopicsFile` and `TemplateTex` must reside in the `config` folder.
- All other files will be stored in the `workdir` folder.
- The `config.ini` file allows you to specify the arXiv section of interest. The default is astrophysics (astro-ph).
- You can modify your topics of interest in `topics.txt` (located in the `config` folder), or any file specified in `config.ini`. The default topics include early stars and hydro simulations.
