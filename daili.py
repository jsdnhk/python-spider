# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
import subprocess as sp
from lxml import etree
import requests
import random
import re

"""
函數說明:獲取IP代理
Parameters:
	page - 高匿代理頁數,默認獲取第一頁
Returns:
	proxys_list - 代理列表
Modify:
	2017-05-27
"""
def get_proxys(page = 1):
	#requests的Session可以自動保持cookie,不需要自己維護cookie內容
	S = requests.Session()
	#西祠代理高匿IP地址
	target_url = 'http://www.xicidaili.com/nn/%d' % page
	#完善的headers
	target_headers = {'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Referer':'http://www.xicidaili.com/nn/',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'zh-CN,zh;q=0.8',
	}
	#get請求
	target_response = S.get(url = target_url, headers = target_headers)
	#utf-8編碼
	target_response.encoding = 'utf-8'
	#獲取網頁信息
	target_html = target_response.text
	#獲取id爲ip_list的table
	bf1_ip_list = BeautifulSoup(target_html, 'lxml')
	bf2_ip_list = BeautifulSoup(str(bf1_ip_list.find_all(id = 'ip_list')), 'lxml')
	ip_list_info = bf2_ip_list.table.contents
	#存儲代理的列表
	proxys_list = []
	#爬取每個代理信息
	for index in range(len(ip_list_info)):
		if index % 2 == 1 and index != 1:
			dom = etree.HTML(str(ip_list_info[index]))
			ip = dom.xpath('//td[2]')
			port = dom.xpath('//td[3]')
			protocol = dom.xpath('//td[6]')
			proxys_list.append(protocol[0].text.lower() + '#' + ip[0].text + '#' + port[0].text)
	#返回代理列表
	return proxys_list

"""
函數說明:檢查代理IP的連通性
Parameters:
	ip - 代理的ip地址
	lose_time - 匹配丟包數
	waste_time - 匹配平均時間
Returns:
	average_time - 代理ip平均耗時
Modify:
	2017-05-27
"""
def check_ip(ip, lose_time, waste_time):
	#命令 -n 要發送的回顯請求數 -w 等待每次回覆的超時時間(毫秒)
	cmd = "ping -n 3 -w 3 %s"
	#執行命令
	p = sp.Popen(cmd % ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True) 
	#獲得返回結果並解碼
	out = p.stdout.read().decode("gbk")
	#丟包數
	lose_time = lose_time.findall(out)
	#當匹配到丟失包信息失敗,默認爲三次請求全部丟包,丟包數lose賦值爲3
	if len(lose_time) == 0:
		lose = 3
	else:
		lose = int(lose_time[0])
	#如果丟包數目大於2個,則認爲連接超時,返回平均耗時1000ms
	if lose > 2:
		#返回False
		return 1000
	#如果丟包數目小於等於2個,獲取平均耗時的時間
	else:
		#平均時間
		average = waste_time.findall(out)
		#當匹配耗時時間信息失敗,默認三次請求嚴重超時,返回平均好使1000ms
		if len(average) == 0:
			return 1000
		else:
			#
			average_time = int(average[0])
			#返回平均耗時
			return average_time

"""
函數說明:初始化正則表達式
Parameters:
	無
Returns:
	lose_time - 匹配丟包數
	waste_time - 匹配平均時間
Modify:
	2017-05-27
"""
def initpattern():
	#匹配丟包數
	lose_time = re.compile(u"丟失 = (\d+)", re.IGNORECASE)
	#匹配平均時間
	waste_time = re.compile(u"平均 = (\d+)ms", re.IGNORECASE)
	return lose_time, waste_time

if __name__ == '__main__':
	#初始化正則表達式
	lose_time, waste_time = initpattern()
	#獲取IP代理
	proxys_list = get_proxys(1)

	#如果平均時間超過200ms重新選取ip
	while True:
		#從100個IP中隨機選取一個IP作爲代理進行訪問
		proxy = random.choice(proxys_list)
		split_proxy = proxy.split('#')
		#獲取IP
		ip = split_proxy[1]
		#檢查ip
		average_time = check_ip(ip, lose_time, waste_time)
		if average_time > 200:
			#去掉不能使用的IP
			proxys_list.remove(proxy)
			print("ip連接超時, 重新獲取中!")
		if average_time < 200:
			break

	#去掉已經使用的IP
	proxys_list.remove(proxy)
	proxy_dict = {split_proxy[0]:split_proxy[1] + ':' + split_proxy[2]}
	print("使用代理:", proxy_dict)
