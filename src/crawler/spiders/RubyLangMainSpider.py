import urlparse
import scrapy
from dateutil import parser
import re

class RubyLangMainSpider(scrapy.Spider):
    name = 'rubylang-main'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_message_groups)

    def choose_parser(self, response):
        if response.url.endswith('index.html'):
            self.parse_message_groups(response)
        elif re.match('^(.*\/[^\/]*\-[^\/]*\.shtml)$') is not None:
            self.parse_message_list(response)
        else:
            self.parse_message(response)

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
        header_raw = response.css('div#header').extract_first()
        header = self.parse_header(header_raw)
        text = response.css('pre').extract_first()

        subject = self.remove_html(header['Subject'])
        user_raw = header['From']
        user = self.remove_html(user_raw.split('&lt;')[-1].split('&gt;')[0]).strip()
        name = self.remove_html(user_raw.split('&lt;')[0])
        date_raw = self.remove_html(header['Date'])
        date = parser.parse(date_raw).strftime('%Y-%m-%d %H:%M:%S %z')
        id = response.url.split('/')[-1]
        channel = response.url.split('/')[-2]
        references = self.remove_html(header['References']).split(' ')
        reply_to = self.remove_html(header['In-reply-to'])

        yield {
            'id': id,
            'channel': channel,
            'user': user,
            'name': name,
            'date': date,
            'references': references,
            'reply-to': reply_to,
            'subject': subject,
            'text': text,
            'url': response.url
        }

    def remove_html(self, string):
        return re.sub(re.compile('<.*?>'), '', string).strip()

    def parse_header(self, header):
        rows = header.split('<br>')
        dict = { 'Subject': '', 'From': '', 'Date': '', 'References': '', 'In-reply-to': '' }
        for row in rows:
            key = row.split(':')[0].strip()
            value = ':'.join(row.split(':')[1:]).strip()
            dict[key] = value
        return dict
