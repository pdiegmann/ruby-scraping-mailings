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

        links = response.css('body > a[href]')
        if links is None or len(links) <= 0: return

        last_link = links[-1]
        if last_link.css('a').extract_first().endswith(u'\u00BB</a>'):
            yield response.follow(last_link.css('::attr(href)').extract_first(), self.parse_thread_list)

    def parse_thread(self, response):
        forum = ''
        thread = ''
        id = ''

        for message_raw in response.css('body > table > tr'):
            message_link = message_raw.css('td.subject > a::attr(href)').extract_first()
            if message_link is not None:
                message_link_parts = message_link.split('/')
            else:
                message_link_parts = [forum, thread, response.url]

            subject = message_raw.css('td.subject > a::text').extract_first()
            user = self.remove_html(message_raw.css('td.author').extract_first())
            date = message_raw.css('td.lastPostDate::text').extract_first()
            html = message_raw.css('td.snippet > div > div').extract_first()
            text = self.remove_html(html)
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
                'html': html,
                'text': text
            }

    def remove_html(self, string):
        if string is None: return ''
        return re.sub(re.compile('<.*?>'), '', unicode(string)).strip()
