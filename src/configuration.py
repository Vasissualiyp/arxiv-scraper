import configparser

class Config:
    def __init__(self, config_file):
        self.parser = configparser.ConfigParser()
        self.parser.read(config_file)

    def __getattr__(self, name):
        if name in self.parser['DEFAULT']:
            return self.parser['DEFAULT'][name]
        raise AttributeError(f"No such configuration option: {name}")

# Example usage
config_file = 'config.ini'  # Replace with your config file path
config = Config(config_file)

# Now you can access your configuration settings like this
arxiv_url = config.arxiv_url
topics_file = config.topics_file
last_paper_file = config.last_paper_file
output_tex_file = config.output_tex_file

