import configuration as config

test_configuration = config.Configuration("config.json")

# Print RSS Feed Links
def print_rss_feed_links():
    for feed in test_configuration.get_rss_feeds():
        print(feed)


# Print Entry Count
def print_entry_count():
    print(test_configuration.get_entrycount_value())

if __name__ == "__main__":
    print_rss_feed_links()
    print_entry_count()