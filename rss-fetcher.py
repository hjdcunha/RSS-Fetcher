from time import sleep
import feedparser
from random import shuffle
from Configuration.configuration import Configuration
import Utilities.utilities as ut


class RSSFetcher:
    def __init__(self, filename):
        self.rss_feed_list = []
        self.rss_data = []

        self.config = Configuration(filename)

    def get_rss_content(self, rss_link):
        rss_feed = feedparser.parse(rss_link)
        return rss_feed.entries

    def get_latest_feeds(self):
        self.rss_list = []
        for link in self.config.get_rss_feeds():
            rss_entry = self.get_rss_content(link)
            self.rss_list = self.rss_list + rss_entry[:self.config.get_entrycount_value()]

    def create_database_data(self):
        self.rss_list = self.scramble_rss_feeds(self.rss_list)
        for i in range(len(self.rss_list)):
            hashtags = ut.generate_hashtags(self.rss_list[i].title)
            self.rss_data.append({
                'title': self.rss_list[i].title,
                'hashtags': hashtags,
                'link': self.rss_list[i].link
            })
        print(len(self.rss_data))

    def scramble_rss_feeds(self, rss_list):
        rss_list = rss_list[:]
        shuffle(rss_list)
        return rss_list

    def get_data(self):
        self.config.reload_config()
        self.get_latest_feeds()
        self.create_database_data()
        return self.rss_data