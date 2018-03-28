import urlparse
import scrapy
from dateutil import parser
import re

class RubyLangMainSpider(scrapy.Spider):
    name = 'rails-main'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_thread_list)

    def parse_thread_list(self, response):
        for thread_link in response.css('td.subject > a::attr(href)').extract():
            forum_name = thread_link.split('/')[-2]
            thread_id = thread_link.split('/')[-1]
            yield response.follow(('https://groups.google.com/forum/?_escaped_fragment_=topic/' + forum_name + '/' + thread_id), self.parse_thread)

        last_link = response.css('body > a[href]')[-1]
        if last_link.css('a').extract_first().endswith(u'\u00BB</a>'):
            print last_link.css('::attr(href)').extract_first()
            yield response.follow(last_link.css('::attr(href)').extract_first(), self.parse_thread_list)

    def parse_thread(self, response):
        for message_raw in response.css('table > tr'):
            message_link_parts = message_raw.css('td.subject > a::attr(href)').extract_first().split('/')
            subject = message_raw.css('td.subject > a::text').extract_first()
            user = message_raw.css('td.author::text').extract_first()
            date = message_raw.css('td.lastPostDate::text').extract_first()
            text = message_raw.css('td.snippet > div > div').extract_first()
            forum = message_link_parts[-3]
            thread = message_link_parts[-2]
            id = message_link_parts[-1]

            yield {
                'id': id,
                'thread': thread,
                'forum': forum,
                'user': user,
                'date': date,
                'subject': subject,
                'text': text
            }

    def remove_html(self, string):
        return re.sub(re.compile('<.*?>'), '', string).strip()
