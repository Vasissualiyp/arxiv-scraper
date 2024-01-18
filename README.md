This is a script that automatically scrapes the newest arxiv papers' abstracts
only with topics, somewhat relevant to what you choose. The relevance is
determined by ChatGPT API. The script then compiles all these abstracts into a
single latex document, so you don't have to
go throug all the new papers and only get info, relevant to your field.

=Installation=
For installation, you will need python, installed with pip. You also need to obtain a 
ChatGPT API for calls to OpenAI servers to categorize papers.

To install, simply run the script:
`./setup.sh`

The script will prompt you for all necessary information, like OpenAI API key,
create a python environment and install all the python libraries.
To get your API key, see: https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/

=Execution=
For running the script, run:
`./run.sh`

The script will scrape arxiv data paper names, use ChatGPT to find papers that
are relevant to your topics, and then extract the abstracts for those papers
from arxiv. It then will compile all those papers into a latex document in the
directory `workdir`. After that, the script will move the tex document to a
folder, specified in the script.

=Configuration=
You can change the names of the documents in the `config.ini` file in the
`config` folder. Keep in mind, that `TopicsFile` and `TemplateTex` must be
located in `config` folder, and all other files will be located in the
`workdir` folder. In the same `config.ini` file you also can change which
section of arxiv you're interested in: by default, it's astrophysics
(astro-ph).

You can change the list of your topics of interest in `topics.txt` in the
`config` folder (or whatever file you set in `config.ini`). Default topics are
related to first stars and hydro simulations.
