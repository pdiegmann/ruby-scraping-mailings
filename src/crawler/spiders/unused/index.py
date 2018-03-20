import urlparse
import scrapy

class IndexSpider(scrapy.Spider):
    name = 'index'
    #start_urls = ['http://blade.nagaokaut.ac.jp/ruby/ruby-core/index.shtml']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for cell in response.css('td'):
            for thread_link in cell.css('a'):

                yield {
                    'id': thread_link.css('::text').extract_first(),
                    'url': urlparse.urljoin(response.url, thread_link.css('::attr(href)').extract_first())
                    }
