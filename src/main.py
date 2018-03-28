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

    if raw_input('crawl ruby-lang mailing lists? [y/N]: ') == 'y':
        process.crawl('rubylang-main', start_urls=['http://blade.nagaokaut.ac.jp/ruby/ruby-core/index.shtml', 'http://blade.nagaokaut.ac.jp/ruby/ruby-talk/index.shtml'])
    elif raw_input('crawl rails mailing lists? [y/N]: ') == 'y':
        process.crawl('rails-main', start_urls=['https://groups.google.com/forum/?_escaped_fragment_=forum/rubyonrails-core'])
    process.start()

if __name__ == "__main__":
    main()
