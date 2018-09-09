# -*- coding: utf-8 -*-
import scrapy

from dateutil import parser
from datetime import timedelta

class EventsClujlifeSpider(scrapy.Spider):
    name = 'events-clujlife'
    allowed_domains = ['clujlife.com']
    start_urls = ['https://www.clujlife.com/evenimente/calendar/?action=tribe_photo&tribe_paged=1&tribe_event_display=photo&tribe-bar-date=2018-05-25']

    def parse(self, response):
        events = response.css(".type-tribe_events[id^='post']")
        date = response.url.split('=')[-1]
        for event in events:
            start_date = event.css('span.tribe-event-date-start::text').extract_first().strip()
            end_date = event.css('span.tribe-event-date-end::text').extract_first().strip()
            yield {
                'date': date,
                'name': event.css('a.tribe-event-url::text').extract_first().strip(),
                'date_range': start_date + ' -- ' + end_date
            }
        base_url = '='.join(response.url.split('=')[:-1])
        new_date = (parser.parse(date) + timedelta(days=1)).strftime('%Y-%m-%d')
        if new_date < '2018-06-01':
            next_url = '{}={}'.format(base_url, new_date) 
            yield scrapy.Request(url=next_url, callback=self.parse)
