# ArXiv Abstract Scraper and Compiler

This script automates the process of scraping the newest arXiv papers' abstracts based on topics relevant to your chosen field. The relevance of papers is determined using the ChatGPT API. It then compiles these abstracts into a single LaTeX document, streamlining access to information pertinent to your research area.

## Installation

### Prerequisites
- Python installed with pip
- An OpenAI API key for accessing the ChatGPT API

### Setup
1. Obtain an OpenAI API key following instructions [here](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/).
2. Run the setup script:
`setup.sh`
This script sets up the environment, asks for your OpenAI API key, and installs necessary Python libraries.

## Execution

To manually run the script, execute:
`run.sh`
This script scrapes arXiv for paper titles, uses ChatGPT to identify relevant papers, extracts their abstracts, and compiles them into a LaTeX document in `workdir`.
After that, it moves the compiled document to a folder, specified in the script. You can change this folder inside of `run.sh`. By default, it moves it into the folder `output`.

## Automated Daily Execution

During setup, you can opt to schedule `run.sh` to execute daily at a specified time. This is done through cron, a time-based job scheduler in Unix-like operating systems. If you choose this option, the script will prompt you to specify the time for daily execution in HH:MM format. This feature is especially useful if the script is deployed on a server.

## Configuration

Edit the `config.ini` file in the `config` folder to customize settings:
- `TopicsFile` and `TemplateTex` should be in the `config` folder.
- Other files will be in the `workdir` folder.
- Change the arXiv section (default is astrophysics, astro-ph) and topics of interest in `topics.txt` or the specified file in `config.ini`.
