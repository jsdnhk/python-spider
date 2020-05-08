# 注：2020年最新連載教程請移步：[Python Spider 2020](https://github.com/Jack-Cherish/python-spider/tree/master/2020 "Python Spider 2020")

# Python Spider

* 貴有恆，何必三更起五更睡；最無益，只怕一日曝十日寒。
* Python3爬蟲實戰：實戰源碼+博客講解
* [個人網站](http://cuijiahua.com "個人網站")
* [CSDN博客](http://blog.csdn.net/c406495762 "CSDN博客")
* [CSDN爬蟲專欄](https://blog.csdn.net/c406495762/article/category/9268672 "爬蟲專欄")<br>
* 學習交流羣【328127489】<a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=e70f3fcff3761450fda9b43eadc1910dac308a962ef9e3e87941cd2c681c4bb4"><img border="0" src="https://github.com/Jack-Cherish/Pictures/blob/master/qqgroup.png" alt="Coder" title="Coder"></a><br>
* 公衆號：[JackCui-AI](https://mp.weixin.qq.com/s/OCWwRVDFNslIuKyiCVUoTA "JackCui-AI")<br>
* 分享技術，樂享生活：Jack Cui公衆號推送“程序員歡樂送”系列資訊類文章，以及技術類文章，歡迎您的關注！
<div align="center"><img border="0" src="https://ww2.sinaimg.cn/large/0072Lfvtly1fxuhd2t2jqj309k09kglk.jpg" alt="Coder" title="gongzhonghao" with="200" height="200"></div>

## 聲明

* 代碼、教程**僅限於學習交流，請勿用於任何商業用途！**

### 文章首發聲明

* 文章在自己的個人網站首發，其他平臺文章均屬轉發，如想獲得最新更新進展，歡迎關注我的個人網站：http://cuijiahua.com/

## 目錄

* [爬蟲小工具](#爬蟲小工具)
    * [文件下載小助手](https://github.com/Jack-Cherish/python-spider/blob/master/downloader.py "懸停顯示")
* [爬蟲實戰](#爬蟲實戰)
    * [筆趣看小說下載](https://github.com/Jack-Cherish/python-spider/blob/master/biqukan.py "懸停顯示")
    * [百度文庫免費文章下載助手_rev1](https://github.com/Jack-Cherish/python-spider/blob/master/baiduwenku.py "懸停顯示")
    * [百度文庫免費文章下載助手_rev2](https://github.com/Jack-Cherish/python-spider/blob/master/baiduwenku_pro_1.py "懸停顯示")
    * [《帥啊》網帥哥圖片下載](https://github.com/Jack-Cherish/python-spider/blob/master/shuaia.py "懸停顯示")
    * [構建代理IP池](https://github.com/Jack-Cherish/python-spider/blob/master/daili.py "懸停顯示")
    * [《火影忍者》漫畫下載](https://github.com/Jack-Cherish/python-spider/tree/master/cartoon "懸停顯示")
    * [財務報表下載小助手](https://github.com/Jack-Cherish/python-spider/blob/master/financical.py "懸停顯示")
    * [一小時入門網絡爬蟲](https://github.com/Jack-Cherish/python-spider/tree/master/one_hour_spider "懸停顯示")
    * [抖音App視頻下載](https://github.com/Jack-Cherish/python-spider/tree/master/douyin "懸停顯示")
    * [GEETEST驗證碼識別](https://github.com/Jack-Cherish/python-spider/blob/master/geetest.py "懸停顯示")
    * [12306搶票小助手](https://github.com/Jack-Cherish/python-spider/blob/master/12306.py "懸停顯示")
    * [百萬英雄答題輔助系統](https://github.com/Jack-Cherish/python-spider/tree/master/baiwan "懸停顯示")   
    * [網易雲音樂免費音樂批量下載](https://github.com/Jack-Cherish/python-spider/tree/master/Netease "懸停顯示")
    * [B站免費視頻和彈幕批量下載](https://github.com/Jack-Cherish/python-spider/tree/master/bilibili "懸停顯示")
    * [京東商品曬單圖下載](https://github.com/Jack-Cherish/python-spider/tree/master/dingdong "懸停顯示")
    * [正方教務管理系統個人信息查詢](https://github.com/Jack-Cherish/python-spider/tree/master/zhengfang_system_spider "懸停顯示")
* [其它](#其它)

## 爬蟲小工具

* downloader.py:文件下載小助手

	一個可以用於下載圖片、視頻、文件的小工具，有下載進度顯示功能。稍加修改即可添加到自己的爬蟲中。
	
	動態示意圖：
	
	![image](https://raw.githubusercontent.com/Jack-Cherish/Pictures/master/9.gif)

## 爬蟲實戰
 
 * biqukan.py:《筆趣看》盜版小說網站，爬取小說工具

	第三方依賴庫安裝：

		pip3 install beautifulsoup4

	使用方法：

		python biqukan.py

 * baiduwenku.py: 百度文庫word文章爬取
	
	原理說明：http://blog.csdn.net/c406495762/article/details/72331737
	
	代碼不完善，沒有進行打包，不具通用性，純屬娛樂。
	
 * shuaia.py: 爬取《帥啊》網，帥哥圖片

	《帥啊》網URL：http://www.shuaia.net/index.html

	原理說明：http://blog.csdn.net/c406495762/article/details/72597755
	
	第三方依賴庫安裝：
	
		pip3 install requests beautifulsoup4
		
 * daili.py: 構建代理IP池

	原理說明：http://blog.csdn.net/c406495762/article/details/72793480
	
	
 * carton: 使用Scrapy爬取《火影忍者》漫畫

	代碼可以爬取整個《火影忍者》漫畫所有章節的內容，保存到本地。更改地址，可以爬取其他漫畫。保存地址可以在settings.py中修改。
	
	動漫網站：http://comic.kukudm.com/
	
	原理說明：http://blog.csdn.net/c406495762/article/details/72858983
	
 * hero.py: 《王者榮耀》推薦出裝查詢小助手

	網頁爬取已經會了，想過爬取手機APP裏的內容嗎？
	
	原理說明：http://blog.csdn.net/c406495762/article/details/76850843
	
 * financical.py: 財務報表下載小助手

	爬取的數據存入數據庫會嗎？《跟股神巴菲特學習炒股之財務報表入庫(MySQL)》也許能給你一些思路。
	
	原理說明：http://blog.csdn.net/c406495762/article/details/77801899
	
	動態示意圖：
	
	![image](https://raw.githubusercontent.com/Jack-Cherish/Pictures/master/10.gif)
	
 * one_hour_spider:一小時入門Python3網絡爬蟲。

	原理說明:
	
	 * 知乎：https://zhuanlan.zhihu.com/p/29809609
	 * CSDN：http://blog.csdn.net/c406495762/article/details/78123502
	
	本次實戰內容有：
	
	 * 網絡小說下載(靜態網站)-biqukan
	 * 優美壁紙下載(動態網站)-unsplash
	 * 視頻下載
	 
 * douyin.py:抖音App視頻下載
 
	抖音App的視頻下載，就是普通的App爬取。

	原理說明:
	
	 * 個人網站：http://cuijiahua.com/blog/2018/03/spider-5.html
	
 * douyin_pro:抖音App視頻下載（升級版）
 
	抖音App的視頻下載，添加視頻解析網站，支持無水印視頻下載，使用第三方平臺解析。

	原理說明:
	
	 * 個人網站：http://cuijiahua.com/blog/2018/03/spider-5.html
	 
 * douyin:抖音App視頻下載（升級版2）
 
	抖音App的視頻下載，添加視頻解析網站，支持無水印視頻下載，通過url解析，無需第三方平臺。
	
	原理說明:
	
	 * 個人網站：http://cuijiahua.com/blog/2018/03/spider-5.html
	 
	動態示意圖：
	
	![image](https://github.com/Jack-Cherish/Pictures/blob/master/14.gif)
	
 * geetest.py:GEETEST驗證碼識別
 
 	原理說明:
	
	 無
	
 * 12306.py:用Python搶火車票簡單代碼
 
	可以自己慢慢豐富，蠻簡單，有爬蟲基礎很好操作，沒有原理說明。
	
 * baiwan:百萬英雄輔助答題
 
	效果圖：
	
	![image](https://github.com/Jack-Cherish/Pictures/blob/master/11.gif)
	
	原理說明：
	
	* 個人網站：http://cuijiahua.com/blog/2018/01/spider_3.html
	
  	功能介紹：
	
	服務器端，使用Python（baiwan.py）通過抓包獲得的接口獲取答題數據，解析之後通過百度知道搜索接口匹配答案，將最終匹配的結果寫入文件（file.txt)。
	
	手機抓包不會的朋友，可以看下我的早期[手機APP抓包教程](http://blog.csdn.net/c406495762/article/details/76850843 "懸停顯示")。
	
	Node.js（app.js）每隔1s讀取一次file.txt文件，並將讀取結果通過socket.io推送給客戶端（index.html）。
	
	親測答題延時在3s左右。
	
	聲明：沒做過後端和前端，花了一天時間，現學現賣弄好的，javascript也是現看現用，百度的程序，調試調試而已。可能有很多用法比較low的地方，用法不對，請勿見怪，有大牛感興趣，可以自行完善。

 * Netease:根據歌單下載網易雲音樂
 	
	效果圖：
	
	![image](https://github.com/Jack-Cherish/Pictures/blob/master/13.gif)
	
	原理說明：
	
	暫無
	
	功能介紹：
	
	根據music_list.txt文件裏的歌單的信息下載網易雲音樂，將自己喜歡的音樂進行批量下載。

 * bilibili：B站視頻和彈幕批量下載
 	
	原理說明：
	
	暫無
	
	使用說明：
	
        python bilibili.py -d 貓 -k 貓 -p 10

        三個參數：
        -d	保存視頻的文件夾名
        -k	B站搜索的關鍵字
        -p	下載搜索結果前多少頁
	
 * jingdong：京東商品曬單圖下載
 
 	效果圖：
	
	![image](https://github.com/Jack-Cherish/Pictures/blob/master/jd.gif)
 	
	原理說明：
	
	暫無
	
	使用說明：
	
        python jd.py -k 芒果
	
         三個參數：
        -d	保存圖片的路徑，默認爲fd.py文件所在文件夾
        -k	搜索關鍵詞
        -n  	下載商品的曬單圖個數，即n個商店的曬單圖

 * zhengfang_system_spider：對正方教務管理系統個人課表，個人學生成績，績點等簡單爬取
 
 	效果圖：
	
	![image](/zhengfang_system_spider/screenshot/zf.png)
 	
	原理說明：
	
	暫無
	
	使用說明：
	
        cd zhengfang_system_spider
        pip install -r requirements.txt
        python spider.py

## 其它

 * 歡迎 Pull requests，感謝貢獻。
