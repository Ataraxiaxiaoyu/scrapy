# -*- coding: utf-8 -*-
import scrapy
import json
from time import sleep
import datetime
import requests
from scrapy.http import Request
from lxml import etree
from pangci.items import PangciItem

class pangciSpider(scrapy.Spider):

	name = "pa"
	allowed_domains = ["www.panc.cc"]
	start_urls = ["https://www.panc.cc",]

	def parse(self,response):

		print('-'*55)
		keyword=input("请输入搜索关键字：\n")

		for i in range(0,5):
			yield Request(url="https://www.panc.cc/panc/api/?s= %s &f=0&t=td&p=%s" % (keyword,str(i)),
			callback=self.page)

	def page(self,response):
		# 调用body_as_unicode()是为了能处理unicode编码的数据
		sites = json.loads(response.body_as_unicode())
		print("-"*60)
		data = sites.get("list")
		
		for dic in data:

			#验证url的有效性
			for short in [dic["shorturl"]]:
				url= "https://pan.baidu.com/s/"+ str(short)
				header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}

				resp = requests.get(url, headers=header ,timeout=5)
				html = etree.HTML(resp.content)
				title =html.xpath("//title/text()")
				#百度网盘链接不存在时的网页标题
				tit ="百度网盘-链接不存在"

				item = PangciItem()
				#当前资源链接是否有效
				if title[0] != tit:

					print('可用链接：',resp.url)
					item["title"] = dic["title"]
					item["shorturl"] = str(resp.url)
					item["date"] = str(datetime.date.today())
					#print(item)
					yield  item

				else:
					#print("网盘链接失效")
					continue



