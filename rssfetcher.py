import feedparser
from random import shuffle
from Configuration.configuration import Configuration
import Utilities.utilities as ut
import Database.database as db


class RSSFetcher:
    def __init__(self, filename):
        self.rss_list = []
        self.rss_data = []
        
        self.config = Configuration(filename)
        self.dbconnector = db.RSSDatabase(self.config)

    # Gets all the latest content from an RSS Feed
    def get_rss_content(self, rss_link):
        rss_feed = feedparser.parse(rss_link)
        return rss_feed.entries

    # Iterates through each RSS Link and stores the contents of that feed (qty determined by the Entry Count)
    # in the rss_list member variable.
    def get_feeds(self):
        self.rss_list = []
        for link in self.config.get_rss_feeds():
            rss_entry = self.get_rss_content(link)
            self.rss_list = self.rss_list + rss_entry[:self.config.get_entrycount_value()]

    # Shuffles the list of RSS Feed items
    # Stores nessary extracted information from an item in an rss_data list ready for Database insertion.
    def create_database_data(self):
        self.rss_list = ut.shuffle_list(self.rss_list)
        for item in self.rss_list:
            hashtags = ut.generate_hashtags(item.title)
            self.rss_data.append({
                'title': item.title,
                'hashtags': hashtags,
                'link': item.link,
                'published_date': item.published
            })

    def cleanup(self):
        self.rss_list.clear()
        self.rss_data.clear()
        self.dbconnector.cleanup_database()

    def get_poll_interval(self):
        return int(self.config.get_poll_interval())

    # Main Class Method to be called by the schedular
    # Reloads the config in case more links are added / links are removed
    # Gets the latest feed data
    # Extracts important information from the feed item
    # Inserts it into the database
    def get_latest_data(self):
        self.config.reload_config()
        self.get_feeds()
        self.create_database_data()
        self.dbconnector.insert_into_data_table(self.rss_data)
        self.dbconnector.insert_into_link_table(self.config.get_rss_feeds())
        self.dbconnector.insert_metrics()
        self.cleanup()