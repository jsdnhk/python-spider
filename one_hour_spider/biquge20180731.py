# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os

"""
從www.biqubao.com筆趣閣爬取小說，樓主教程中的網址我當時沒打開，
就參照樓主教程，爬取了筆趣閣小說網的內容。
    2018-07-31
"""

if __name__=='__main__':
    #所要爬取的小說主頁，每次使用時，修改該網址即可，同時保證本地保存根路徑存在即可
    target="https://www.biqubao.com/book/17570/"
    # 本地保存爬取的文本根路徑
    save_path = 'G:/pythonlearn'
    #筆趣閣網站根路徑
    index_path='https://www.biqubao.com'

    req=requests.get(url=target)
    #查看request默認的編碼，發現與網站response不符，改爲網站使用的gdk
    print(req.encoding)
    req.encoding = 'gbk'
    #解析html
    soup=BeautifulSoup(req.text,"html.parser")
    list_tag=soup.div(id="list")
    print('list_tag:',list_tag)
    #獲取小說名稱
    story_title=list_tag[0].dl.dt.string
    # 根據小說名稱創建一個文件夾,如果不存在就新建
    dir_path=save_path+'/'+story_title
    if not os.path.exists(dir_path):
        os.path.join(save_path,story_title)
        os.mkdir(dir_path)
    #開始循環每一個章節，獲取章節名稱，與章節對應的網址
    for dd_tag in list_tag[0].dl.find_all('dd'):
        #章節名稱
        chapter_name=dd_tag.string
        #章節網址
        chapter_url=index_path+dd_tag.a.get('href')
        #訪問該章節詳情網址，爬取該章節正文
        chapter_req = requests.get(url=chapter_url)
        chapter_req.encoding = 'gbk'
        chapter_soup = BeautifulSoup(chapter_req.text, "html.parser")
        #解析出來正文所在的標籤
        content_tag = chapter_soup.div.find(id="content")
        #獲取正文文本，並將空格替換爲換行符
        content_text = str(content_tag.text.replace('\xa0','\n'))
        #將當前章節，寫入以章節名字命名的txt文件
        with open(dir_path+'/'+chapter_name+'.txt', 'w') as f:
            f.write('本文網址:'+chapter_url)
            f.write(content_text)