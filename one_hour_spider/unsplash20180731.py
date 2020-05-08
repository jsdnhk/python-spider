# -*- coding:utf-8 -*-
import requests
import json
import os
from contextlib import closing

"""
從https://unsplash.com/爬取壁紙代碼，使用時我是開啓了代理軟件
國內網速貌似有些限制，很慢
    2018-07-31
"""

# 本地保存圖片根路徑（請確保根路徑存在）
save_path = 'G:/pythonlearn'
dir_path=save_path+'/'+'unsplash-image'
if not os.path.exists(dir_path):
    os.path.join(save_path, 'unsplash-image')
    os.mkdir(dir_path)
n=10
#n建議從第2頁開始，因爲第一頁的per_page可能是1，不是12
while n>2:
    print('當前爬取第'+str(n)+'次加載圖片（本次共12張）')
    url='https://unsplash.com/napi/photos?page='+str(n)+'&per_page=12&order_by=latest'
    req=requests.get(url=url)
    html=json.loads(req.text)
    for each in html:
        downloadurl=each['links']["download"]
        jpgrep=requests.get(url=downloadurl)
        with closing(requests.get(url=downloadurl, stream=True)) as r:
            with open(dir_path+'/'+each['id']+'.jpg', 'ab+') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
    n=n-1