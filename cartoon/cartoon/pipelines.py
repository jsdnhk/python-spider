# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from cartoon import settings
from scrapy import Request
import requests
import os


class ComicImgDownloadPipeline(object):

	def process_item(self, item, spider):
		#如果獲取了圖片鏈接，進行如下操作
		if 'img_url' in item:
			images = []
			#文件夾名字
			dir_path = '%s/%s' % (settings.IMAGES_STORE, item['dir_name'])
			#文件夾不存在則創建文件夾
			if not os.path.exists(dir_path):
				os.makedirs(dir_path)
			#獲取每一個圖片鏈接
			for image_url in item['img_url']:
				#解析鏈接，根據鏈接爲圖片命名
				houzhui = image_url.split('/')[-1].split('.')[-1]
				qianzhui = item['link_url'].split('/')[-1].split('.')[0]
				#圖片名
				image_file_name = '第' + qianzhui + '頁.' + houzhui
				#圖片保存路徑
				file_path = '%s/%s' % (dir_path, image_file_name)
				images.append(file_path)
				if os.path.exists(file_path):
					continue
				#保存圖片
				with open(file_path, 'wb') as handle:
					response = requests.get(url = image_url)
					for block in response.iter_content(1024):
						if not block:
							break
						handle.write(block)
			#返回圖片保存路徑
			item['image_paths'] = images
		return item