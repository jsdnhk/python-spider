# -*- coding:utf-8 -*-
from tkinter.filedialog import askdirectory
from MyQR.myqr import run
from urllib import request, parse
from bs4 import BeautifulSoup

import tkinter.messagebox as msgbox
import tkinter as tk
import webbrowser
import re
import json
import os
import types
import requests
import time


"""
類說明:愛奇藝、優酷等實現在線觀看以及視頻下載的類

Parameters:
	width - tkinter主界面寬
	height - tkinter主界面高

Returns:
	無

Modify:
	2017-05-09
"""
class APP:
	def __init__(self, width = 500, height = 300):
		self.w = width
		self.h = height
		self.title = ' VIP視頻破解助手'
		self.root = tk.Tk(className=self.title)
		self.url = tk.StringVar()
		self.v = tk.IntVar()
		self.v.set(1)


		#Frame空間
		frame_1 = tk.Frame(self.root)
		frame_2 = tk.Frame(self.root)
		frame_3 = tk.Frame(self.root)
		
		#Menu菜單
		menu = tk.Menu(self.root)
		self.root.config(menu = menu)
		filemenu = tk.Menu(menu,tearoff=0)
		moviemenu = tk.Menu(menu,tearoff = 0)
		menu.add_cascade(label = '菜單', menu = filemenu)
		menu.add_cascade(label = '友情鏈接', menu = moviemenu)
		filemenu.add_command(label = '使用說明',command = lambda :webbrowser.open('http://blog.csdn.net/c406495762/article/details/71334633'))
		filemenu.add_command(label = '關於作者',command = lambda :webbrowser.open('http://blog.csdn.net/c406495762'))
		filemenu.add_command(label = '退出',command = self.root.quit)

		#各個網站鏈接
		moviemenu.add_command(label = '網易公開課',command = lambda :webbrowser.open('http://open.163.com/'))
		moviemenu.add_command(label = '騰訊視頻',command = lambda :webbrowser.open('http://v.qq.com/'))
		moviemenu.add_command(label = '搜狐視頻',command = lambda :webbrowser.open('http://tv.sohu.com/'))
		moviemenu.add_command(label = '芒果TV',command = lambda :webbrowser.open('http://www.mgtv.com/'))
		moviemenu.add_command(label = '愛奇藝',command = lambda :webbrowser.open('http://www.iqiyi.com/'))
		moviemenu.add_command(label = 'PPTV',command = lambda :webbrowser.open('http://www.bilibili.com/'))
		moviemenu.add_command(label = '優酷',command = lambda :webbrowser.open('http://www.youku.com/'))
		moviemenu.add_command(label = '樂視',command = lambda :webbrowser.open('http://www.le.com/'))
		moviemenu.add_command(label = '土豆',command = lambda :webbrowser.open('http://www.tudou.com/'))
		moviemenu.add_command(label = 'A站',command = lambda :webbrowser.open('http://www.acfun.tv/'))
		moviemenu.add_command(label = 'B站',command = lambda :webbrowser.open('http://www.bilibili.com/'))

		#控件內容設置
		group = tk.Label(frame_1,text = '請選擇一個視頻播放通道：', padx = 10, pady = 10)
		tb1 = tk.Radiobutton(frame_1,text = '通道一', variable = self.v, value = 1, width = 10, height = 3)
		tb2 = tk.Radiobutton(frame_1,text = '通道二', variable = self.v, value = 2, width = 10, height = 3)
		label1 = tk.Label(frame_2, text = "請輸入視頻鏈接：")
		entry = tk.Entry(frame_2, textvariable = self.url, highlightcolor = 'Fuchsia', highlightthickness = 1,width = 35)
		label2 = tk.Label(frame_2, text = " ")
		play = tk.Button(frame_2, text = "播放", font = ('楷體',12), fg = 'Purple', width = 2, height = 1, command = self.video_play)
		label3 = tk.Label(frame_2, text = " ")
		# download = tk.Button(frame_2, text = "下載", font = ('楷體',12), fg = 'Purple', width = 2, height = 1, command = self.download_wmxz)
		QR_Code = tk.Button(frame_3, text = "手機觀看", font = ('楷體',12), fg = 'Purple', width = 10, height = 2, command = self.QR_Code)
		label_explain = tk.Label(frame_3, fg = 'red', font = ('楷體',12), text = '\n注意：支持大部分主流視頻網站的視頻播放！\n此軟件僅用於交流學習，請勿用於任何商業用途！')
		label_warning = tk.Label(frame_3, fg = 'blue', font = ('楷體',12),text = '\n建議：將Chrome內核瀏覽器設置爲默認瀏覽器\n作者:Jack_Cui')



		#控件佈局
		frame_1.pack()
		frame_2.pack()
		frame_3.pack()
		group.grid(row = 0, column = 0)
		tb1.grid(row = 0, column = 1)
		tb2.grid(row = 0, column = 2)
		label1.grid(row = 0, column = 0)
		entry.grid(row = 0, column = 1)
		label2.grid(row = 0, column = 2)
		play.grid(row = 0, column = 3,ipadx = 10, ipady = 10)
		label3.grid(row = 0, column = 4)
		# download.grid(row = 0, column = 5,ipadx = 10, ipady = 10)
		QR_Code.grid(row = 0, column = 0)
		label_explain.grid(row = 1, column = 0)
		label_warning.grid(row = 2, column = 0)

	"""
	函數說明:jsonp解析

	Parameters:
		_jsonp - jsonp字符串

	Returns:
		_json - json格式數據

	Modify:
		2017-05-11
	"""
	def loads_jsonp(self, _jsonp):
		try:
			_json = json.loads(re.match(".*?({.*}).*",_jsonp,re.S).group(1))
			return _json
		except:
			raise ValueError('Invalid Input')

	"""
	函數說明:視頻播放

	Parameters:
		self

	Returns:
		無

	Modify:
		2017-05-09
	"""
	def video_play(self):
		#視頻解析網站地址
		port_1 = 'http://www.wmxz.wang/video.php?url='
		port_2 = 'http://www.vipjiexi.com/tong.php?url='

		#正則表達是判定是否爲合法鏈接
		if re.match(r'^https?:/{2}\w.+$', self.url.get()):
			if self.v.get() == 1:
				#視頻鏈接獲取
				ip = self.url.get()
				#視頻鏈接加密
				ip = parse.quote_plus(ip)
				#瀏覽器打開
				webbrowser.open(port_1 + self.url.get())
			elif self.v.get() == 2:
				#鏈接獲取
				ip = self.url.get()
				#鏈接加密
				ip = parse.quote_plus(ip)

				#獲取time、key、url
				get_url = 'http://www.vipjiexi.com/x2/tong.php?url=%s' % ip 
				# get_url_head = {
				# 	'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
				# 	'Referer':'http://www.vipjiexi.com/',
				# }
				# get_url_req = request.Request(url = get_url, headers = get_url_head)
				# get_url_response = request.urlopen(get_url_req)
				# get_url_html = get_url_response.read().decode('utf-8')
				# bf = BeautifulSoup(get_url_html, 'lxml')
				# a = str(bf.find_all('script'))
				# pattern = re.compile('"api.php", {"time":"(\d+)", "key": "(.+)", "url": "(.+)","type"', re.IGNORECASE)
				# string = pattern.findall(a)
				# now_time = string[0][0]
				# now_key = string[0][1]
				# now_url = string[0][2] 

				# #請求播放,獲取Success = 1
				# get_movie_url = 'http://www.vipjiexi.com/x2/api.php'
				# get_movie_data = {
				# 	'key':'%s' % now_key,
				# 	'time':'%s' % now_time,
				# 	'type':'',
				# 	'url':'%s' % now_url
				# }
				# get_movie_head = {
				# 	'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
				# 	'Referer':'http://www.vipjiexi.com/x2/tong.php?',
				# 	'url':'%s' % ip,
				# }
				# get_movie_req = request.Request(url = get_movie_url, headers = get_movie_head)
				# get_movie_data = parse.urlencode(get_movie_data).encode('utf-8')
				# get_movie_response = request.urlopen(get_movie_req, get_movie_data)
				#請求之後立刻打開
				webbrowser.open(get_url)

		else:
			msgbox.showerror(title='錯誤',message='視頻鏈接地址無效，請重新輸入！')

	"""
	函數說明:視頻下載，通過無名小站抓包(已經無法使用)

	Parameters:
		self

	Returns:
		無

	Modify:
		2017-06-15
	"""
	def download_wmxz(self):	
		if re.match(r'^https?:/{2}\w.+$', self.url.get()):
			#視頻鏈接獲取
			ip = self.url.get()
			#視頻鏈接加密
			ip = parse.quote_plus(ip)

			#獲取保存視頻的url
			get_url = 'http://www.sfsft.com/index.php?url=%s' % ip 
			head = {
				'User-Agent':'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
				'Referer':'http://www.sfsft.com/index.php?url=%s' % ip
			}
			get_url_req = request.Request(url = get_url, headers = head)
			get_url_response = request.urlopen(get_url_req)
			get_url_html = get_url_response.read().decode('utf-8')
			bf = BeautifulSoup(get_url_html, 'lxml')
			a = str(bf.find_all('script'))
			pattern = re.compile("url : '(.+)',", re.IGNORECASE)
			url = pattern.findall(a)[0]

			#獲取視頻地址
			get_movie_url = 'http://www.sfsft.com/api.php'
			get_movie_data = {
				'up':'0',
				'url':'%s' % url,
			}
			get_movie_req = request.Request(url = get_movie_url, headers = head)
			get_movie_data = parse.urlencode(get_movie_data).encode('utf-8')
			get_movie_response = request.urlopen(get_movie_req, get_movie_data)
			get_movie_html = get_movie_response.read().decode('utf-8')
			get_movie_data = json.loads(get_movie_html)
			webbrowser.open(get_movie_data['url'])
		else:
			msgbox.showerror(title='錯誤',message='視頻鏈接地址無效，請重新輸入！')


	"""
	函數說明:生成二維碼,手機觀看

	Parameters:
		self

	Returns:
		無

	Modify:
		2017-05-12
	"""
	def QR_Code(self):	
		if re.match(r'^https?:/{2}\w.+$', self.url.get()):
			#視頻鏈接獲取
			ip = self.url.get()
			#視頻鏈接加密
			ip = parse.quote_plus(ip)

			url = 'http://www.wmxz.wang/video.php?url=%s' % ip
			words = url
			images_pwd = os.getcwd() + '\Images\\'
			png_path = images_pwd + 'bg.png'
			qr_name = 'qrcode.png'
			qr_path = images_pwd + 'qrcode.png'

			run(words = words, picture = png_path, save_name = qr_name, save_dir = images_pwd)

			top = tk.Toplevel(self.root)
			img = tk.PhotoImage(file = qr_path)
			text_label = tk.Label(top, fg = 'red', font = ('楷體',15), text = "手機瀏覽器掃描二維碼，在線觀看視頻！")
			img_label = tk.Label(top, image = img)
			text_label.pack()
			img_label.pack()
			top.mainloop()

		else:
			msgbox.showerror(title='錯誤',message='視頻鏈接地址無效，請重新輸入！')

	"""
	函數說明:tkinter窗口居中

	Parameters:
		self

	Returns:
		無

	Modify:
		2017-05-09
	"""
	def center(self):
		ws = self.root.winfo_screenwidth()
		hs = self.root.winfo_screenheight()
		x = int( (ws/2) - (self.w/2) )
		y = int( (hs/2) - (self.h/2) )
		self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))

	"""
	函數說明:loop等待用戶事件

	Parameters:
		self

	Returns:
		無

	Modify:
		2017-05-09
	"""
	def loop(self):
		self.root.resizable(False, False)	#禁止修改窗口大小
		self.center()						#窗口居中
		self.root.mainloop()

if __name__ == '__main__':
	app = APP()			#實例化APP對象
	app.loop()			#loop等待用戶事件




