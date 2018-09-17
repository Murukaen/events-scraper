# -*- coding: utf-8 -*-
import scrapy

class BaseSpider(scrapy.Spider):

    RO_MONTHS = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie', 
        'iulie', 'august', 'septembrie', 'octombrie', 'noiembrie', 'decembrie']

    def get_description(self, elem):
        """ Concatenate text from a list of <p> Selectors """
        ret = ''
        for p in elem:
            text = p.css('::text').extract_first()
            if text:
                ret += text
        return ret

    def format_datetime(self, year, month, day, hours='00', minutes='00'):
        return '{0}-{1}-{2}T{3}:{4}:00Z'.format(str(year), str(month).zfill(2), str(day).zfill(2), 
            str(hours).zfill(2), str(minutes).zfill(2))