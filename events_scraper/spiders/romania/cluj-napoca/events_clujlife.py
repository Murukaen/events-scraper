# -*- coding: utf-8 -*-
import scrapy

from dateutil import parser
from datetime import timedelta
from events_scraper.spiders.romania.ro_base_spider import RoBaseSpider

class EventsClujlifeSpider(RoBaseSpider):
    name = 'events-clujlife'
    allowed_domains = ['clujlife.com']
    url = 'https://www.clujlife.com/evenimente/calendar/?action=tribe_photo&tribe_paged=1&tribe_event_display=photo&tribe-bar-date='
    city = 'Cluj-Napoca'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [self.url + self.start_date]

    def local_format_datetime(self, date):
        terms = date.replace(',',' ').split()
        year = '2018'
        if len(terms) == 5:
            year = terms[2]
        month = self.RO_MONTHS.index(terms[1].lower()) + 1
        day = terms[0]
        if len(terms) == 2:
            return self.format_datetime_parts(year, month, day)
        else:
            time = terms[-2].split(':')
            hours = time[0]
            minutes = time[1]
            if (terms[-1] == 'pm'):
                hours = str(int(hours) + 12)
            return self.format_datetime_parts(year, month, day, hours, minutes)  

    def parse_details(self, response):
        yield {
            'name': response.css('h1.tribe-events-single-event-title::text').extract_first(),
            'startDate': self.local_format_datetime(response.css('.dtstart::text').extract_first()),
            'endDate': self.local_format_datetime(response.css('.dtend::text').extract_first()),
            'location': response.css('.tribe-venue > a::text').extract_first(),
            'description': self.get_description(response.css('.tribe-events-content > p')),
            'createdBy': self.author,
            'country': self.country,
            'city': self.city
        }

    def parse(self, response):
        event_urls = response.css('.type-tribe_events[id^="post"] a.tribe-event-url::attr(href)').extract()
        for url in event_urls:
            yield scrapy.Request(url=url, callback=self.parse_details)
        date = response.url.split('=')[-1]
        base_url = '='.join(response.url.split('=')[:-1])
        new_date = (parser.parse(date) + timedelta(days=1)).strftime('%Y-%m-%d')
        if new_date <= self.end_date:
            next_url = '{}={}'.format(base_url, new_date) 
            yield scrapy.Request(url=next_url, callback=self.parse)
