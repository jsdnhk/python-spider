# -*- coding:utf-8 -*-
from contextlib import closing
import requests, json, re, os, sys
import urllib

class DouYin(object):
	def __init__(self, width = 500, height = 300):
		"""
		抖音App視頻下載
		"""
		self.headers = {
			'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-origin',
			'accept': 'application/json',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'zh-CN,zh;q=0.9',
		}
		self.headers1 = {
			'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
		}

	def get_video_urls(self, user_id, type_flag='f'):
		"""
		獲得視頻播放地址
		Parameters:
			user_id：查詢的用戶UID
		Returns:
			video_names: 視頻名字列表
			video_urls: 視頻鏈接列表
			nickname: 用戶暱稱
		"""
		video_names = []
		video_urls = []
		share_urls = []
		max_cursor = 0
		has_more = 1
		sign_api = 'http://49.233.200.77:5001'
		share_user_url = 'https://www.iesdouyin.com/share/user/%s' % user_id
		share_user = requests.get(share_user_url, headers=self.headers)
		while share_user.status_code != 200:
			share_user = requests.get(share_user_url, headers=self.headers)
		_tac_re = re.compile(r"tac='([\s\S]*?)'</script>")
		tac = _tac_re.search(share_user.text).group(1)
		_dytk_re = re.compile(r"dytk\s*:\s*'(.+)'")
		dytk = _dytk_re.search(share_user.text).group(1)
		_nickname_re = re.compile(r'<p class="nickname">(.+?)<\/p>')
		nickname = _nickname_re.search(share_user.text).group(1)
		data = {
			'tac': tac.split('|')[0],
			'user_id': user_id,
		}
		req = requests.post(sign_api, data=data)
		while req.status_code != 200:
			req = requests.post(sign_api, data=data)
		sign = req.json().get('signature')
		user_url_prefix = 'https://www.iesdouyin.com/web/api/v2/aweme/like' if type_flag == 'f' else 'https://www.iesdouyin.com/web/api/v2/aweme/post'
		print('解析視頻鏈接中')
		while has_more != 0:
			user_url = user_url_prefix + '/?user_id=%s&sec_uid=&count=21&max_cursor=%s&aid=1128&_signature=%s&dytk=%s' % (user_id, max_cursor, sign, dytk)
			req = requests.get(user_url, headers=self.headers)
			while req.status_code != 200:
				req = requests.get(user_url, headers=self.headers)
			html = json.loads(req.text)
			for each in html['aweme_list']:
				try:
					url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=%s&line=0&ratio=720p&media_type=4&vr_type=0&improve_bitrate=0&is_play_url=1&is_support_h265=0&source=PackSourceEnum_PUBLISH'
					vid = each['video']['vid']
					video_url = url % vid
				except:
					continue
				share_desc = each['desc']
				if os.name == 'nt':
					for c in r'\/:*?"<>|':
						nickname = nickname.replace(c, '').strip().strip('\.')
						share_desc = share_desc.replace(c, '').strip()
				share_id = each['aweme_id']
				if share_desc in ['抖音-原創音樂短視頻社區', 'TikTok', '']:
					video_names.append(share_id + '.mp4')
				else:
					video_names.append(share_id + '-' + share_desc + '.mp4')
				share_url = 'https://www.iesdouyin.com/share/video/%s' % share_id
				share_urls.append(share_url)
				video_urls.append(video_url)
			max_cursor = html['max_cursor']
			has_more = html['has_more']

		return video_names, video_urls, share_urls, nickname

	def get_download_url(self, video_url, watermark_flag):
		"""
		獲得帶水印的視頻播放地址
		Parameters:
			video_url：帶水印的視頻播放地址
		Returns:
			download_url: 帶水印的視頻下載地址
		"""
		# 帶水印視頻
		if watermark_flag == True:
			download_url = video_url.replace('/play/', '/playwm/')
		# 無水印視頻
		else:
			download_url = video_url.replace('/playwm/', '/play/')

		return download_url

	def video_downloader(self, video_url, video_name, watermark_flag=False):
		"""
		視頻下載
		Parameters:
			video_url: 帶水印的視頻地址
			video_name: 視頻名
			watermark_flag: 是否下載帶水印的視頻
		Returns:
			無
		"""
		size = 0
		video_url = self.get_download_url(video_url, watermark_flag=watermark_flag)
		with closing(requests.get(video_url, headers=self.headers1, stream=True)) as response:
			chunk_size = 1024
			content_size = int(response.headers['content-length'])
			if response.status_code == 200:
				sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))

				with open(video_name, 'wb') as file:
					for data in response.iter_content(chunk_size = chunk_size):
						file.write(data)
						size += len(data)
						file.flush()

						sys.stdout.write('  [下載進度]:%.2f%%' % float(size / content_size * 100) + '\r')
						sys.stdout.flush()

	def run(self):
		"""
		運行函數
		Parameters:
			None
		Returns:
			None
		"""
		self.hello()
		print('UID取得方式：\n分享用戶頁面，用瀏覽器打開短鏈接，原始鏈接中/share/user/後的數字即是UID')
		user_id = input('請輸入UID (例如60388937600):')
		user_id = user_id if user_id else '60388937600'
		watermark_flag = input('是否下載帶水印的視頻 (0-否(默認), 1-是):')
		watermark_flag = watermark_flag if watermark_flag!='' else '0'
		watermark_flag = bool(int(watermark_flag))
		type_flag = input('f-收藏的(默認), p-上傳的:')
		type_flag = type_flag if type_flag!='' else 'f'
		save_dir = input('保存路徑 (例如"E:/Download/", 默認"./Download/"):')
		save_dir = save_dir if save_dir else "./Download/"
		video_names, video_urls, share_urls, nickname = self.get_video_urls(user_id, type_flag)
		nickname_dir = os.path.join(save_dir, nickname)
		if not os.path.exists(save_dir):
			os.makedirs(save_dir)
		if nickname not in os.listdir(save_dir):
			os.mkdir(nickname_dir)
		if type_flag == 'f':
			if 'favorite' not in os.listdir(nickname_dir):
				os.mkdir(os.path.join(nickname_dir, 'favorite'))
		print('視頻下載中:共有%d個作品!\n' % len(video_urls))
		for num in range(len(video_urls)):
			print('  解析第%d個視頻鏈接 [%s] 中，請稍後!\n' % (num + 1, share_urls[num]))
			if '\\' in video_names[num]:
				video_name = video_names[num].replace('\\', '')
			elif '/' in video_names[num]:
				video_name = video_names[num].replace('/', '')
			else:
				video_name = video_names[num]
			video_path = os.path.join(nickname_dir, video_name) if type_flag!='f' else os.path.join(nickname_dir, 'favorite', video_name)
			if os.path.isfile(video_path):
				print('視頻已存在')
			else:
				self.video_downloader(video_urls[num], video_path, watermark_flag)
			print('\n')
		print('下載完成!')

	def hello(self):
		"""
		打印歡迎界面
		Parameters:
			None
		Returns:
			None
		"""
		print('*' * 100)
		print('\t\t\t\t抖音App視頻下載小助手')
		print('\t\t作者:Jack Cui、steven7851')
		print('*' * 100)


if __name__ == '__main__':
	douyin = DouYin()
	douyin.run()
