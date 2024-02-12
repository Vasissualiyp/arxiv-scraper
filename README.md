# ArXiv Abstract Scraper and Compiler

This script automates the process of scraping the newest arXiv papers' abstracts based on topics relevant to your chosen field. The relevance of papers is determined using the ChatGPT API. It then compiles these abstracts into a single LaTeX document, streamlining access to information pertinent to your research area. This script also has the ability to generate a voice reading of the papers, using text-to-speech python library.

## Installation

### Prerequisites
- Python installed with pip
- An OpenAI API key for accessing the ChatGPT API
- bash utilities: pdflatex, poppler-utils

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
- Change the ChatGPT model (so far `gpt-3.5-turbo` is the default, which is cheap but sometimes gets things wrong. `gpt-4` is better but more expensive)

## YouTube Video Uploader
This tool allows you to upload videos to YouTube either from a desktop environment or a headless server. It uses OAuth 2.0 for authentication with Google's YouTube API v3. You can enable an option to upload the video of your scraping results in the `config.ini` file.

The source code for the uploader is in `src/upload_yt_video.py`.

An example of YouTube channel that uses this daily automatic upload procedure is: https://www.youtube.com/channel/UCcyy48vdToDKAqlm-343VNw


### Setting Up

Before you start, make sure you have completed the following steps:

1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. 2. Create a project.
3. 3. Enable the YouTube Data API v3 for your project.
4. 4. Create OAuth 2.0 credentials for a Desktop application.
5. 5. Download the credentials and save them as `./config/credentials.json` in your project directory.
6. 6. Add your email to the OAuth consent screen.
### Installation

Ensure you have Python 3.x installed and then install the required libraries using pip:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

(These libraries are also were installed if you ran the `setup.sh` script)

### Authentication and Credentials Storage

#### Desktop Authentication

First, authenticate and save your credentials on a desktop environment using the provided Python script. The script will guide you through the authentication process and save your credentials in a file named `token.pickle` within the `./config` directory.

This process only needs to be completed once. The credentials will be refreshed automatically as needed.

#### Using Credentials on a Headless Server

After obtaining the `token.pickle` file on your desktop, transfer this file to your headless server. Place it in the same `./config` directory relative to the script. The script will use these credentials to authenticate without user interaction.

### Uploading Videos

To upload a video, ensure your video file is accessible to the script and modify the video file path and metadata in the script as needed.

#### Running the Script

Execute the script with Python:

```bash
python upload_yt_video.py
```

The script will automatically handle authentication using the saved credentials and proceed to upload your video to YouTube.

### Security Note

Please handle the `credentials.json` and `token.pickle` files securely. Do not share these files or expose them publicly. Ensure they are stored in a secure location with limited access.

### Troubleshooting

- If authentication fails, try deleting the `token.pickle` file and re-authenticating on a desktop environment.
- Ensure your `credentials.json` file is correctly configured and corresponds to a Desktop application in the Google Developers Console.
- - Check that the YouTube Data API v3 is enabled for your Google Cloud project.
- Adjust the paths and filenames as necessary to match your project's structure and naming conventions. This README provides a comprehensive guide for users to authenticate and use your YouTube video uploader tool in various environments.
