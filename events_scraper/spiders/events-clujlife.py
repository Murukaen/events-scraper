# -*- coding: utf-8 -*-
import scrapy

from dateutil import parser
from datetime import timedelta

class EventsClujlifeSpider(scrapy.Spider):
    name = 'event-clujlife'
    allowed_domains = ['clujlife.com']
    url = 'https://www.clujlife.com/evenimente/calendar/?action=tribe_photo&tribe_paged=1&tribe_event_display=photo&tribe-bar-date='
    start_date = '2018-09-15'
    stop_date = '2018-09-15'

    def __init__(self):
        self.start_urls = [self.url + self.start_date]

    def get_description(self, elem):
        ret = ''
        for p in elem:
            text = p.css('::text').extract_first()
            if text:
                ret += text
        return ret

    def parse_details(self, response):
        yield {
            'name': response.css('h1.tribe-events-single-event-title::text').extract_first(),
            'start_date': response.css('.dtstart::text').extract_first(),
            'end_date': response.css('.dtend::text').extract_first(),
            'location': response.css('.tribe-venue > a::text').extract_first(),
            'description': self.get_description(response.css('.tribe-events-content > p'))
        }

    def parse(self, response):
        event_urls = response.css('.type-tribe_events[id^="post"] a.tribe-event-url::attr(href)').extract()
        for url in event_urls:
            yield scrapy.Request(url=url, callback=self.parse_details)
        date = response.url.split('=')[-1]
        base_url = '='.join(response.url.split('=')[:-1])
        new_date = (parser.parse(date) + timedelta(days=1)).strftime('%Y-%m-%d')
        if new_date <= self.stop_date:
            next_url = '{}={}'.format(base_url, new_date) 
            yield scrapy.Request(url=next_url, callback=self.parse)
