import urlparse
import scrapy

class IndexSpider(scrapy.Spider):
    name = 'main'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_message_groups)

    def choose_parser(self, response):
        if response.url.endswith('index.html'):
            parse_message_groups(self, response)
        elif re.match('^(.*\/[^\/]*\-[^\/]*\.shtml)$') is not None:
            parse_message_list(self, response)
        else:
            parse_message(self, response)

    def parse_message_groups(self, response):
        for cell in response.css('td'):
            for thread_link in cell.css('a'):
                yield response.follow(urlparse.urljoin(response.url, thread_link.css('::attr(href)').extract_first()), self.parse_message_list)

    def parse_message_list(self, response):
        for cell in response.css('DT'):
            for message_link in cell.css('a[href]'):
                if message_link.css('::attr(href)').extract_first().startswith('#'):
                    continue

                yield response.follow(urlparse.urljoin(response.url, message_link.css('::attr(href)').extract_first()), self.parse_message)

    def parse_message(self, response):
        header = response.css('div#header').extract_first()
        header_parts = header.split('<br>')
        text = response.css('pre').extract_first()

        yield {
            'user': ':'.join(header_parts[2].split(':')[1:]).strip(),
            'date': ':'.join(header_parts[3].split(':')[1:]).strip(),
            'subject': ':'.join(header_parts[1].split(':')[1:]).strip(),
            'text': text
        }
