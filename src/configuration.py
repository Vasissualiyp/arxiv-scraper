import configparser
import os

print("Current working directory:", os.getcwd())


class Config:
    def __init__(self, config_file):
        self.parser = configparser.ConfigParser()
        self.parser.read(config_file)
        self.config_file = config_file

    def __getattr__(self, name):
        if self.parser.has_option('DEFAULT', name):
            return self.parser.get('DEFAULT', name)
        raise AttributeError(f"No such configuration option: {name}")

    def __setattr__(self, name, value):
        if name in ["parser", "config_file"]:
            super().__setattr__(name, value)
        else:
            self.parser.set('DEFAULT', name, value)

    def save(self):
        with open(self.config_file, 'w') as configfile:
            self.parser.write(configfile)

def extract_configuration(config_file):
    # Example usage
    with open(config_file, 'r') as file:
        line = file.read()
    print(line)
    config = Config(config_file)
    
    # Change the locations of the documents to their respecitve folders
    config.TopicsFile = os.path.join('config', config.TopicsFile)
    config.TemplateTex = os.path.join('config', config.TemplateTex)
    config.LastPaperFile = os.path.join('workdir', config.LastPaperFile)
    config.RelatedPapersJson  = os.path.join('workdir', config.RelatedPapersJson )
    config.RelatedPapersContent  = os.path.join('workdir', config.RelatedPapersContent )
    config.OutputTexFile = os.path.join('workdir', config.OutputTexFile)

    return config
