import sqlite3
import os
from datetime import datetime

class RSSDatabase:

    def __init__(self, config):
        self.config = config
        self.create_db()
        self.create_tables()
    
    def create_db(self):
        self.db = sqlite3.connect(self.config.get_database_location())
        self.db_cursor = self.db.cursor()

    def create_tables(self):
        try:
            # Data Table
            self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS Data(
                    Id INTEGER PRIMARY KEY,
                    PostTitle TEXT UNIQUE,
                    PostLink TEXT,
                    PostPublishedDate TEXT,
                    PostHashtags TEXT,
                    EntryDate DATETIME DEFAULT (datetime('now','localtime'))
                )
            ''')
            self.db.commit()

        except Exception as e:
            print("Data Table Creation Error: {0}", e)

        try:
            # Links Table
            self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS Links(
                    Id INTEGER PRIMARY KEY,
                    FeedLink TEXT,
                    UpdatedDate DATETIME DEFAULT (datetime('now','localtime'))
                )
            ''')
            self.db.commit()

        except Exception as e:
            print("Data Table Creation Error: {0}", e)

        try:
            # Metrics Table
            self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS Metrics(
                    Id INTEGER PRIMARY KEY,
                    ActiveLinks INTEGER,
                    ActiveRows INTEGER,
                    DatabaseSize TEXT,
                    UpdatedDate DATETIME DEFAULT (datetime('now','localtime'))
                )
            ''')
            self.db.commit()

        except Exception as e:
            print("Data Table Creation Error: {0}", e)

    def delete_database(self):
        try:
            os.remove('rss-fetcher-database.db')

        except Exception as e:
            print("Delete Database Exepction: {0}", e)

    def insert_into_data_table(self, data):
        for item in data:
            try:
                self.db_cursor.execute('''
                    INSERT INTO Data(PostTitle, PostLink, PostPublishedDate, PostHashtags)
                    VALUES(?,?,?,?)''', (item['title'],item['link'],item['published_date'],item['hashtags']))
            except Exception:
                pass
            self.db.commit()

    def insert_into_link_table(self, links):
        try:
            self.db_cursor.execute('''
            DELETE FROM Links
            ''')
        except Exception as e:
            print("Error Deleting Records from Link Table {0}", e)

        for link in links:
            try:
                self.db_cursor.execute('''
                    INSERT INTO Links(FeedLink)
                    VALUES(?)''', (link,))
            except Exception as e:
                print("Error Inserting Links: {0} {1}", e, datetime.now())
            self.db.commit()

    def insert_metrics(self):
        try:
            self.db_cursor.execute('''
                SELECT COUNT (*) from data
            ''')
            active_rows = self.db_cursor.fetchone()

            self.db_cursor.execute
            self.db_cursor.execute('''
                SELECT COUNT (*) from links
            ''')
            active_links = self.db_cursor.fetchone()
            database_size = os.stat(self.config.get_database_location()).st_size

            self.db_cursor.execute('''
                    INSERT INTO Metrics(ActiveLinks, ActiveRows, DatabaseSize)
                    VALUES(?,?,?)''', (int(active_links[0]), int(active_rows[0]), database_size))

        except Exception as e:
            print("Error Inserting Metrics: {0}", e)
        self.db.commit()

    def cleanup_database(self):
        print("Data Count: " + str(self.get_data_count()))
        print("Max Data Row Count: " + str(self.config.get_max_data_rows()))
        if(self.get_data_count() > self.config.get_max_data_rows()):
            try:
                self.db_cursor.execute('''
                    SELECT Id from Data ORDER BY Id LIMIT 1
                ''')

                oldest_post_id = self.db_cursor.fetchone()
                print("Oldest Post ID: " + str(oldest_post_id[0]))

                to_remove_count = self.get_data_count() - int(self.config.get_max_data_rows())
                print("To Remove Count: " + str(to_remove_count))

                for i in range(int(oldest_post_id[0]), int(oldest_post_id[0]) + to_remove_count):
                    self.db_cursor.execute('''
                        DELETE FROM Data WHERE Id=?
                    ''', (i,))
                self.db.commit()
                
                print("New Row Count: " + str(self.get_data_count()))

            except Exception as e:
                print(e)

    def get_data_count(self):
        try:
            self.db_cursor.execute('''
                SELECT COUNT (*) from data
            ''')
            data_count = self.db_cursor.fetchone()
            return int(data_count[0])
        except Exception as e:
            print('Error getting Data Table Row Count.')