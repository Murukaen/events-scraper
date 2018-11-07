import scrapy

class BaseSpider(scrapy.Spider):
    def format_datetime_parts(self, year, month, day, hours='00', minutes='00'):
        return '{0}-{1}-{2}T{3}:{4}:00Z'.format(str(year), str(month).zfill(2), str(day).zfill(2), 
            str(hours).zfill(2), str(minutes).zfill(2))
    def format_datetime(self, dt):
        return dt.strftime("%Y-%m-%dT%H:%M:%S:00Z")
    