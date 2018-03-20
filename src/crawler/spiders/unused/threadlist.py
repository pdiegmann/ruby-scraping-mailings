import urlparse
import scrapy

class ThreadListpider(scrapy.Spider):
    name = 'threadlist'
    #start_urls = ['http://blade.nagaokaut.ac.jp/ruby/ruby-core/82001-82200.shtml']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for cell in response.css('DT'):
            for message_link in cell.css('a[href]'):
                if message_link.css('::attr(href)').extract_first().startswith('#'):
                    continue

                yield {
                    'id': message_link.css('::text').extract_first(),
                    'url': urlparse.urljoin(response.url, message_link.css('::attr(href)').extract_first())
                    }
