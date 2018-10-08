# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class PangciPipeline(object):

	def __init__(self):
		self.file = open("./res.json",'a+',encoding="utf-8")



	def process_item(self, item, spider):
		data = json.dumps(dict(item),ensure_ascii=False)+';\n'
		self.file.write(data)
		return item

#print(type(dict(item)))#data = pickle.dumps(item)
		#print(type(item))
		#print(type(data))
	def spider_closed(self,spider):
		self.file.close()
