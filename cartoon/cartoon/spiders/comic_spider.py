# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy import Selector
from cartoon.items import ComicItem

class ComicSpider(scrapy.Spider):
	name = 'comic'

	def __init__(self):
		#圖片鏈接server域名
		self.server_img = 'http://n.1whour.com/'
		#章節鏈接server域名
		self.server_link = 'http://comic.kukudm.com'
		self.allowed_domains = ['comic.kukudm.com']
		self.start_urls = ['http://comic.kukudm.com/comiclist/3/']
		#匹配圖片地址的正則表達式
		self.pattern_img = re.compile(r'\+"(.+)\'><span')

	#從start_requests發送請求
	def start_requests(self):
		yield scrapy.Request(url = self.start_urls[0], callback = self.parse1)

	#解析response,獲得章節圖片鏈接地址
	def parse1(self, response):
		hxs = Selector(response)
		items = []
		#章節鏈接地址
		urls = hxs.xpath('//dd/a[1]/@href').extract()
		#章節名
		dir_names = hxs.xpath('//dd/a[1]/text()').extract()
		#保存章節鏈接和章節名
		for index in range(len(urls)):
			item = ComicItem()
			item['link_url'] = self.server_link + urls[index]
			item['dir_name'] = dir_names[index]
			items.append(item)

		#根據每個章節的鏈接，發送Request請求，並傳遞item參數
		for item in items:
			yield scrapy.Request(url = item['link_url'], meta = {'item':item}, callback = self.parse2)
		
	#解析獲得章節第一頁的頁碼數和圖片鏈接	
	def parse2(self, response):
		#接收傳遞的item
		item = response.meta['item']
		#獲取章節的第一頁的鏈接
		item['link_url'] = response.url
		hxs = Selector(response)
		#獲取章節的第一頁的圖片鏈接
		pre_img_url = hxs.xpath('//script/text()').extract()
		#注意這裏返回的圖片地址,應該爲列表,否則會報錯
		img_url = [self.server_img + re.findall(self.pattern_img, pre_img_url[0])[0]]
		#將獲取的章節的第一頁的圖片鏈接保存到img_url中
		item['img_url'] = img_url
		#返回item，交給item pipeline下載圖片
		yield item
		#獲取章節的頁數
		page_num = hxs.xpath('//td[@valign="top"]/text()').re(u'共(\d+)頁')[0]
		#根據頁數，整理出本章節其他頁碼的鏈接
		pre_link = item['link_url'][:-5]
		for each_link in range(2, int(page_num) + 1):
			new_link = pre_link + str(each_link) + '.htm'
			#根據本章節其他頁碼的鏈接發送Request請求，用於解析其他頁碼的圖片鏈接，並傳遞item
			yield scrapy.Request(url = new_link, meta = {'item':item}, callback = self.parse3)

	#解析獲得本章節其他頁面的圖片鏈接
	def parse3(self, response):
		#接收傳遞的item
		item = response.meta['item']
		#獲取該頁面的鏈接
		item['link_url'] = response.url
		hxs = Selector(response)
		pre_img_url = hxs.xpath('//script/text()').extract()
		#注意這裏返回的圖片地址,應該爲列表,否則會報錯
		img_url = [self.server_img + re.findall(self.pattern_img, pre_img_url[0])[0]]
		#將獲取的圖片鏈接保存到img_url中
		item['img_url'] = img_url
		#返回item，交給item pipeline下載圖片
		yield item
		