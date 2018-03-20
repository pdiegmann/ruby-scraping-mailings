import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import jsonlines
import os
import shutil
import datetime

data_folder = os.path.join('..', 'data')
archive_folder = os.path.join('..', 'archive')
process = CrawlerProcess(get_project_settings())

def main():
    print "starting"

    if os.path.exists(data_folder):
        shutil.move(data_folder, os.path.join(archive_folder, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))

    process.crawl('main', start_urls=['http://blade.nagaokaut.ac.jp/ruby/ruby-core/index.shtml'])
    process.start()

if __name__ == "__main__":
    main()
