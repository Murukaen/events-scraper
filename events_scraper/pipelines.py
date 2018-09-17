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

    def process_item(self, item, spider):
        item = dict(item)
        item['country'] = self.country
        item['city'] = self.city
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
