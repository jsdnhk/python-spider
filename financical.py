#-*- coding:UTF-8 -*-
import sys
import pymysql
import requests
import json
import re
from bs4 import BeautifulSoup

"""
類說明:獲取財務數據

Author:
	Jack Cui
Blog:
	http://blog.csdn.net/c406495762
Zhihu:
	https://www.zhihu.com/people/Jack--Cui/
Modify:
	2017-08-31
"""
class FinancialData():

	def __init__(self):
		#服務器域名
		self.server = 'http://quotes.money.163.com/'
		self.cwnb = 'http://quotes.money.163.com/hkstock/cwsj_'
		#主要財務指標
		self.cwzb_dict = {'EPS':'基本每股收益','EPS_DILUTED':'攤薄每股收益','GROSS_MARGIN':'毛利率',
		'CAPITAL_ADEQUACY':'資本充足率','LOANS_DEPOSITS':'貸款回報率','ROTA':'總資產收益率',
		'ROEQUITY':'淨資產收益率','CURRENT_RATIO':'流動比率','QUICK_RATIO':'速動比率',
		'ROLOANS':'存貸比','INVENTORY_TURNOVER':'存貨週轉率','GENERAL_ADMIN_RATIO':'管理費用比率',
		'TOTAL_ASSET2TURNOVER':'資產週轉率','FINCOSTS_GROSSPROFIT':'財務費用比率','TURNOVER_CASH':'銷售現金比率','YEAREND_DATE':'報表日期'}
		#利潤表
		self.lrb_dict = {'TURNOVER':'總營收','OPER_PROFIT':'經營利潤','PBT':'除稅前利潤',
		'NET_PROF':'淨利潤','EPS':'每股基本盈利','DPS':'每股派息',
		'INCOME_INTEREST':'利息收益','INCOME_NETTRADING':'交易收益','INCOME_NETFEE':'費用收益','YEAREND_DATE':'報表日期'}
		#資產負債表
		self.fzb_dict = {
			'FIX_ASS':'固定資產','CURR_ASS':'流動資產','CURR_LIAB':'流動負債',
			'INVENTORY':'存款','CASH':'現金及銀行存結','OTHER_ASS':'其他資產',
			'TOTAL_ASS':'總資產','TOTAL_LIAB':'總負債','EQUITY':'股東權益',
			'CASH_SHORTTERMFUND':'庫存現金及短期資金','DEPOSITS_FROM_CUSTOMER':'客戶存款',
			'FINANCIALASSET_SALE':'可供出售之證券','LOAN_TO_BANK':'銀行同業存款及貸款',
			'DERIVATIVES_LIABILITIES':'金融負債','DERIVATIVES_ASSET':'金融資產','YEAREND_DATE':'報表日期'}
		#現金流表
		self.llb_dict = {
			'CF_NCF_OPERACT':'經營活動產生的現金流','CF_INT_REC':'已收利息','CF_INT_PAID':'已付利息',
			'CF_INT_REC':'已收股息','CF_DIV_PAID':'已派股息','CF_INV':'投資活動產生現金流',
			'CF_FIN_ACT':'融資活動產生現金流','CF_BEG':'期初現金及現金等價物','CF_CHANGE_CSH':'現金及現金等價物淨增加額',
			'CF_END':'期末現金及現金等價物','CF_EXCH':'匯率變動影響','YEAREND_DATE':'報表日期'}
		#總表
		self.table_dict = {'cwzb':self.cwzb_dict,'lrb':self.lrb_dict,'fzb':self.fzb_dict,'llb':self.llb_dict}
		#請求頭
		self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
	
	"""
	函數說明:獲取股票頁面信息

	Author:
		Jack Cui
	Parameters:
	    url - 股票財務數據界面地址
	Returns:
	    name - 股票名
	    table_name_list - 財務報表名稱
	    table_date_list - 財務報表年限
	    url_list - 財務報表查詢連接
	Blog:
		http://blog.csdn.net/c406495762
	Zhihu:
		https://www.zhihu.com/people/Jack--Cui/
	Modify:
		2017-08-31
	"""
	def get_informations(self, url):
		req = requests.get(url = url, headers = self.headers)
		req.encoding = 'utf-8'
		html = req.text
		page_bf = BeautifulSoup(html, 'lxml')
		#股票名稱，股票代碼
		name = page_bf.find_all('span', class_ = 'name')[0].string
		# code = page_bf.find_all('span', class_ = 'code')[0].string
		# code = re.findall('\d+',code)[0]

		#存儲各個表名的列表
		table_name_list = []
		table_date_list = []
		each_date_list = []
		url_list = []
		#表名和表時間
		table_name = page_bf.find_all('div', class_ = 'titlebar3')
		for each_table_name in table_name:
			#表名
			table_name_list.append(each_table_name.span.string)
			#表時間
			for each_table_date in each_table_name.div.find_all('select', id = re.compile('.+1$')):
				url_list.append(re.findall('(\w+)1',each_table_date.get('id'))[0])
				for each_date in each_table_date.find_all('option'):
					each_date_list.append(each_date.string)
				table_date_list.append(each_date_list)
				each_date_list = []
		return name,table_name_list,table_date_list,url_list

	"""
	函數說明:財務報表入庫

	Author:
		Jack Cui
	Parameters:
	    name - 股票名
	    table_name_list - 財務報表名稱
	    table_date_list - 財務報表年限
	    url_list - 財務報表查詢連接
	Returns:
		無
	Blog:
		http://blog.csdn.net/c406495762
	Zhihu:
		https://www.zhihu.com/people/Jack--Cui/
	Modify:
		2017-08-31
	"""
	def insert_tables(self, name, table_name_list,table_date_list, url_list):
		#打開數據庫連接:host-連接主機地址,port-端口號,user-用戶名,passwd-用戶密碼,db-數據庫名,charset-編碼
		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yourpasswd',db='financialdata',charset='utf8')
		#使用cursor()方法獲取操作遊標
		cursor = conn.cursor()  
		#插入信息
		for i in range(len(table_name_list)):
			sys.stdout.write('    [正在下載       ]    %s' % table_name_list[i] + '\r')
			#獲取數據地址
			url = self.server + 'hk/service/cwsj_service.php?symbol={}&start={}&end={}&type={}&unit=yuan'.format(code,table_date_list[i][-1],table_date_list[i][0],url_list[i])
			req_table = requests.get(url = url, headers = self.headers)
			table = req_table.json()
			nums = len(table)
			value_dict = {}
			for num in range(nums):
				sys.stdout.write('    [正在下載 %.2f%%]   ' % (((num+1) / nums)*100) + '\r')
				sys.stdout.flush()
				value_dict['股票名'] = name
				value_dict['股票代碼'] = code
				for key, value in table[i].items():
					if key in self.table_dict[url_list[i]]:
						value_dict[self.table_dict[url_list[i]][key]] = value

				sql1 = """
				INSERT INTO %s (`股票名`,`股票代碼`,`報表日期`) VALUES ('%s','%s','%s')""" % (url_list[i],value_dict['股票名'],value_dict['股票代碼'],value_dict['報表日期'])
				try:
					cursor.execute(sql1)
					# 執行sql語句
					conn.commit()
				except:
					# 發生錯誤時回滾
					conn.rollback()

				for key, value in value_dict.items():
					if key not in ['股票名','股票代碼','報表日期']:
						sql2 = """
						UPDATE %s SET %s='%s' WHERE `股票名`='%s' AND `報表日期`='%s'""" % (url_list[i],key,value,value_dict['股票名'],value_dict['報表日期'])
						try:
							cursor.execute(sql2)
							# 執行sql語句
							conn.commit()
						except:
							# 發生錯誤時回滾
							conn.rollback()
				value_dict = {}
			print('    [下載完成 ')

		# 關閉數據庫連接
		cursor.close()  
		conn.close()

if __name__ == '__main__':
	print('*' * 100)
	print('\t\t\t\t\t財務數據下載助手\n')
	print('作者:Jack-Cui\n')
	print('About Me:\n')
	print('  知乎:https://www.zhihu.com/people/Jack--Cui')
	print('  Blog:http://blog.csdn.net/c406495762')
	print('  Gihub:https://github.com/Jack-Cherish\n')
	print('*' * 100)
	fd = FinancialData()
	#上市股票地址
	code = input('請輸入股票代碼:')

	name,table_name_list,table_date_list,url_list = fd.get_informations(fd.cwnb + code + '.html')
	print('\n  %s:(%s)財務數據下載中！\n' % (name,code))
	fd.insert_tables(name,table_name_list,table_date_list,url_list)
	print('\n  %s:(%s)財務數據下載完成！' % (name,code))