import sqlite3

class RSSDatabase:

    def __init__(self):
        self.create_db()
        self.create_tables()
    
    def create_db(self):
        self.db = sqlite3.connect('rss-fetcher-database.db')
        self.db_cursor = self.db.cursor()

    def create_tables(self):
        try:
            # Feeds
            self.db_cursor.execute("CREATE TABLE PROFILE (ID INTEGER PRIMARY KEY AUTOINCREMENT, FollowerCount VARCHAR(30) NOT NULL, FollowingCount VARCHAR(30) NOT NULL, UnfollowingCount VARCHAR(30) NOT NULL, EntryDate DATETIME DEFAULT (datetime('now','localtime')))")
        except Exception as e:
            print("Profile Table Creation Error: {0}", e)

        try:
            #Unfollowed Table - List of people the Bot has Unfollowed
            self.db_cursor.execute("CREATE TABLE UNFOLLOWED (ID INTEGER PRIMARY KEY AUTOINCREMENT, UserID VARCHAR(25) NOT NULL, Username VARCHAR(30) NOT NULL, UnfollowedDate DATETIME DEFAULT (datetime('now','localtime')))")
        except Exception as e:
            print("Unfollowed Table Creation Error: {0}", e)