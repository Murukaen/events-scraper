# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json        
import urllib.request

class ConstructPayload():

    country = 'Romania'
    city = 'Cluj-Napoca'
    ro_months = ['Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie', 
        'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie']

    def formatDate(self, date):
        terms = date.replace(',',' ').split()
        year = '2018'
        if len(terms) == 5:
            year = terms[2]
        month = str(self.ro_months.index(terms[1]) + 1).zfill(2)
        day = terms[0].zfill(2)
        date = '{0}-{1}-{2}'.format(year, month, day)
        if len(terms) == 2:
            return '{0}T00:00:00Z'.format(date)
        else:
            time = terms[-2].split(':')
            hours = time[0]
            minutes = time[1]
            if (terms[-1] == 'pm'):
                hours = str(int(hours) + 12)
            hours = hours.zfill(2)
            minutes = minutes.zfill(2)
            time = '{0}:{1}:00'.format(hours, minutes)
            return '{0}T{1}Z'.format(date, time)

    def rename_dict_key(self, d, old_k, new_k):
        d[new_k] = d[old_k]
        del d[old_k]

    def process_item(self, item, spider):
        item = dict(item)
        item['country'] = self.country
        item['city'] = self.city
        self.rename_dict_key(item, 'start_date', 'startDate')
        item['startDate'] = self.formatDate(item['startDate'])
        self.rename_dict_key(item, 'end_date', 'endDate')
        item['endDate'] = self.formatDate(item['endDate'])
        item['createdBy'] = 'LnPWPpTL4biC8P4Wq' # id of razzvan.savu@gmail.com
        if len(item['location'].strip()) == 0:
            item['location'] = '-'
        if len(item['description'].strip()) == 0:
            item['description'] = '-'
        return item

class CallApi():

    def open_spider(self, spider):
        self.log = open('log', 'w')

    def close_spider(self, spider):
        self.log.close()

    def process_item(self, item, spider):
        myurl = "http://localhost:3000/api/insert"
        req = urllib.request.Request(myurl)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(dict(item))
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        req.add_header('Content-Length', len(jsondataasbytes))
        # print (jsondataasbytes)
        self.log.write('[sending] {0}\n'.format(jsondata))
        response = urllib.request.urlopen(req, jsondataasbytes)
        self.log.write('[response] {0}\n'.format(response.status))
        return item


class JsonWriterPipeline():

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
