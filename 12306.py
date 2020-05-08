# -*- coding: utf-8 -*-
"""
@author: liuyw
"""
from splinter.browser import Browser
from time import sleep
import traceback
import time, sys

class huoche(object):
	driver_name = ''
	executable_path = ''
	#用戶名，密碼
	username = u"xxx"
	passwd = u"xxx"
	# cookies值得自己去找, 下面兩個分別是瀋陽, 哈爾濱
	starts = u"%u6C88%u9633%2CSYT"
	ends = u"%u54C8%u5C14%u6EE8%2CHBB"
	
	# 時間格式2018-01-19
	dtime = u"2018-01-19"
	# 車次，選擇第幾趟，0則從上之下依次點擊
	order = 0
	###乘客名
	users = [u"xxx",u"xxx"]
	##席位
	xb = u"二等座"
	pz = u"成人票"

	"""網址"""
	ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
	login_url = "https://kyfw.12306.cn/otn/login/init"
	initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
	buy = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
	
	def __init__(self):
		self.driver_name = 'chrome'
		self.executable_path = 'D:/chromedriver'

	def login(self):
		self.driver.visit(self.login_url)
		self.driver.fill("loginUserDTO.user_name", self.username)
		# sleep(1)
		self.driver.fill("userDTO.password", self.passwd)
		print(u"等待驗證碼，自行輸入...")
		while True:
			if self.driver.url != self.initmy_url:
				sleep(1)
			else:
				break

	def start(self):
		self.driver = Browser(driver_name=self.driver_name,executable_path=self.executable_path)
		self.driver.driver.set_window_size(1400, 1000)
		self.login()
		# sleep(1)
		self.driver.visit(self.ticket_url)
		try:
			print(u"購票頁面開始...")
			# sleep(1)
			# 加載查詢信息
			self.driver.cookies.add({"_jc_save_fromStation": self.starts})
			self.driver.cookies.add({"_jc_save_toStation": self.ends})
			self.driver.cookies.add({"_jc_save_fromDate": self.dtime})

			self.driver.reload()

			count = 0
			if self.order != 0:
				while self.driver.url == self.ticket_url:
					self.driver.find_by_text(u"查詢").click()
					count += 1
					print(u"循環點擊查詢... 第 %s 次" % count)
					# sleep(1)
					try:
						self.driver.find_by_text(u"預訂")[self.order - 1].click()
					except Exception as e:
						print(e)
						print(u"還沒開始預訂")
						continue
			else:
				while self.driver.url == self.ticket_url:
					self.driver.find_by_text(u"查詢").click()
					count += 1
					print(u"循環點擊查詢... 第 %s 次" % count)
					# sleep(0.8)
					try:
						for i in self.driver.find_by_text(u"預訂"):
							i.click()
							sleep(1)
					except Exception as e:
						print(e)
						print(u"還沒開始預訂 %s" % count)
						continue
			print(u"開始預訂...")
			# sleep(3)
			# self.driver.reload()
			sleep(1)
			print(u'開始選擇用戶...')
			for user in self.users:
				self.driver.find_by_text(user).last.click()

			print(u"提交訂單...")
			sleep(1)
			self.driver.find_by_text(self.pz).click()
			self.driver.find_by_id('').select(self.pz)
			# sleep(1)
			self.driver.find_by_text(self.xb).click()
			sleep(1)
			self.driver.find_by_id('submitOrder_id').click()
			print(u"開始選座...")
			self.driver.find_by_id('1D').last.click()
			self.driver.find_by_id('1F').last.click()

			sleep(1.5)
			print(u"確認選座...")
			self.driver.find_by_id('qr_submit_id').click()

		except Exception as e:
			print(e)

if __name__ == '__main__':
	huoche = huoche()
	huoche.start()