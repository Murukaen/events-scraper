# -*- coding: utf-8 -*-
import scrapy

from dateutil import parser
from datetime import timedelta
from .base_spider import BaseSpider

class EventsClujComSpider(BaseSpider):
    name = 'events-clujcom'
    allowed_domains = ['cluj.com']
    url = 'https://cluj.com/evenimente/'
    start_date = '2018-09-20'
    end_date = '2018-09-20'

    def __init__(self):
        self.start_urls = [self.url + self.start_date]

    def parse_details(self, response):
        date = response.css('.dtstart::text').extract_first().strip()
        time = response.css('.tribe-recurring-event-time::text').extract_first() # can be null
        year = '2018'
        date_terms = date.split()
        month = str(self.RO_MONTHS.index(date_terms[1]) + 1)
        day = date_terms[0]
        if (time):
            time_terms = list(map(lambda s: s.strip(), time.split('-')))
            [start_hours, start_minutes] = time_terms[0].split(':')
            if(len(time_terms) == 2):
                [end_hours, end_minutes] = time_terms[1].split(':')
            else:
                [end_hours, end_minutes] = [str(int(start_hours)+1), start_minutes] # can overflow to next day
        else:
            [start_hours, start_minutes] = [0, 0]
            [end_hours, end_minutes] = [23, 59]
        start_date_time = self.format_datetime(year, month, day, start_hours, start_minutes)
        end_date_time = self.format_datetime(year, month, day, end_hours, end_minutes)
        location = response.css('.tribe-venue > a::text').extract_first() # can be null
        if (not location):
            location = '-'
        yield {
            'name': response.css('h1.tribe-events-single-event-title::text').extract_first(),
            'startDate': start_date_time,
            'endDate': end_date_time,
            'location': location,
            'description': self.get_description(response.css('div.tribe-events-content > p'))
        }

    def parse(self, response):
        event_urls = response.css('.type-tribe_events a.tribe-event-url::attr(href)').extract()
        for url in event_urls:
            yield scrapy.Request(url=url, callback=self.parse_details)
        split_url = response.url.split('/')
        date = split_url[-2]
        new_date = (parser.parse(date) + timedelta(days=1)).strftime('%Y-%m-%d')
        if new_date <= self.end_date:
            next_url = '/'.join(split_url[:-2] + [new_date])
            yield scrapy.Request(url=next_url, callback=self.parse)
