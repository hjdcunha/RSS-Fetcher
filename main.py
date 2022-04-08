import rssfetcher
import schedule
from time import sleep
import sys

def main():
    fetcher = rssfetcher.RSSFetcher(sys.argv[1])
    #fetcher.get_latest_data()

    schedule.every(30).seconds.do(fetcher.get_latest_data)

    while True:
        schedule.run_pending()
        sleep(1)

if __name__ == "__main__":
    main()