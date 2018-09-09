# -*- coding: utf-8 -*-
import scrapy

from dateutil import parser
from datetime import timedelta

class EventsSpider(scrapy.Spider):
    name = 'events-clujcom'
    allowed_domains = ['cluj.com']
    start_urls = ['https://cluj.com/evenimente/2018-05-27/']

    def parse(self, response):
        events = response.css('.type-tribe_events')
        for event in events:
            yield {
                'name': event.css('a.tribe-event-url::attr(title)').extract_first(),
                'start_date': event.css('.tribe-event-date-start::text').extract_first()
            }
        split_url = response.url.split('/')
        date = split_url[-2]
        new_date = (parser.parse(date) + timedelta(days=1)).strftime('%Y-%m-%d')
        if new_date < '2018-06-01':
            next_url = '/'.join(split_url[:-2] + [new_date])
            yield scrapy.Request(url=next_url, callback=self.parse)
