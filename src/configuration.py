import configparser
import os

print("Current working directory:", os.getcwd())


class Config:
    def __init__(self, config_file):
        self.parser = configparser.ConfigParser()
        self.parser.read(config_file)

    def __getattr__(self, name):
        # Convert attribute name to the same case as INI keys
        name = name.lower()
        if self.parser.has_option('DEFAULT', name):
            return self.parser.get('DEFAULT', name)
        raise AttributeError(f"No such configuration option: {name}")


# Example usage
config_file = 'config/config.ini'  # Replace with your config file path
with open(config_file, 'r') as file:
    line = file.read()
print(line)
config = Config(config_file)

# Now you can access your configuration settings like this
arxiv_url = config.ArxivURL
topics_file = config.TopicsFile
last_paper_file = config.LastPaperFile
output_tex_file = config.OutputTexFile

print(arxiv_url)
