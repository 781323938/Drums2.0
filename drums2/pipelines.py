# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from drums2.items import MiniVarInfo

class MongoDBPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["KG"]
        db.drop_collection('drums2')
        self.tempCol = db["drums2"]

    def process_item(self, item, spider):
        """ 判断类型 存入MongoDB """
        if isinstance(item, MiniVarInfo):
            #rint 'HospitalsspidersItem True'
            self.tempCol.insert(dict(item))

        return item
