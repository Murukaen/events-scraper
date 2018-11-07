# -*- coding: utf-8 -*-

from events_scraper.spiders.base_spider import BaseSpider

class RoBaseSpider(BaseSpider):

    RO_MONTHS = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie', 
        'iulie', 'august', 'septembrie', 'octombrie', 'noiembrie', 'decembrie']

    country = 'Romania'

    def __init__(self, *args, **kwargs):
        self.start_date = kwargs['start_date']
        self.end_date = kwargs['end_date']
        self.author = kwargs['author']

    def get_description(self, elem):
        """ Concatenate text from a list of <p> Selectors """
        ret = ''
        for p in elem:
            text = p.css('::text').extract_first()
            if text:
                ret += text
        return ret
