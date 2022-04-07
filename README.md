# RSS-Fetcher
 A tool to get the latest posts from various RSS Feeds defined in a JSON file; and store them in an SQL Database.

## POC 1:
- in rss-fetcher.py need to create an insert method
    - calls get data
    - inserts into the database
    - clears the lists

- in database script
    - define create tables
    - define insert into each table
    - check if exisits before inserting (validate against title)
    - create database cleanup method
