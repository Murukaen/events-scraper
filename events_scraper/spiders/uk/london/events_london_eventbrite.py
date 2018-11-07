import scrapy
import re
from dateutil import parser
from events_scraper.spiders.base_spider import BaseSpider

class EventsLondonEventbrite(BaseSpider):
    name = 'events-london-eventbrite'
    allowed_domains = ['eventbrite.co.uk', 'eventbrite.com']
    # In the url below:
    #   {0} -> startDate
    #   {1} -> endDate
    #   {2} -> page number
    url = 'https://www.eventbrite.co.uk/d/united-kingdom--london/all-events/?end_date={1}&lc=1&mode=search&page={2}&start_date={0}'
    country = 'UK'
    city = 'London'

    def __init__(self, *args, **kwargs):
        self.start_date = kwargs['start_date']
        self.end_date = kwargs['end_date']
        self.author = kwargs['author']
        self.start_urls = [self.url.format(self.start_date, self.end_date,1)]
        self.download_delay = 2

    def parse_details(self, response):
        # start_datetime & end_datetime formats: string: '2018-10-21T12:30:00+01:00'
        start_datetime = response.css('.event-details__data meta:nth-of-type(1)::attr(content)').extract_first()
        end_datetime = response.css('.event-details__data meta:nth-of-type(2)::attr(content)').extract_first()
        yield {
            'name': response.css('h1.listing-hero-title::text').extract_first(),
            'startDate': self.format_datetime(parser.parse(start_datetime)),
            'endDate': self.format_datetime(parser.parse(end_datetime)),
            'location': '-',
            'description': '-',
            'createdBy': self.author,
            'country': self.country,
            'city': self.city
        }
    
    def parse(self, response):
        event_urls = response.css('.eds-media-card-content__image-container a.eds-media-card-content__action-link::attr(href)').extract()
        for url in event_urls:
            yield scrapy.Request(url=url, callback=self.parse_details)
        last_page_number = response.css('[data-spec=paginator__last-page-link] a::text').extract_first()
        if last_page_number != None:
            last_page_number = int(last_page_number)
            current_page_number = int(re.search('page=(.+)&', response.url).group(1))
            print("---->", current_page_number, last_page_number)
            if current_page_number < last_page_number:
                next_url = self.url.format(self.start_date, self.end_date, current_page_number + 1)
                yield scrapy.Request(url=next_url, callback=self.parse)