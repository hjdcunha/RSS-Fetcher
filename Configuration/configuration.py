import json

class Configuration:
    def __init__(self, filename):
        self.filename = filename
        # Opens configuration file and loads data into self.config
        self.reload_config()

    def get_rss_feeds(self):
        # Returns a list of RSS Feed Links as per config.json
        return self.config['rssfeeds']

    def get_entrycount_value(self):
        # Returns an integer value for the Entry Count
        return self.config['entrycount']

    def reload_config(self):
        self.config = None
        data = open(self.filename)
        self.config = json.load(data)

    def get_poll_interval(self):
        return self.config['pollinterval']
