## 功能

下載B站視頻和彈幕，將xml原生彈幕轉換爲ass彈幕文件，支持plotplayer等播放器的彈幕播放。

## 作者

* Website: [http://cuijiahua.com](http://cuijiahua.com "懸停顯示")
* Author: Jack Cui
* Date: 2018.6.12

## 更新

* 2018.09.12：添加FFmpeg分段視頻合併

## 使用說明

FFmpeg下載，並配置環境變量。http://ffmpeg.org/

	python bilibili.py -d 貓 -k 貓 -p 10

	三個參數：
	-d	保存視頻的文件夾名
	-k	B站搜索的關鍵字
	-p	下載搜索結果前多少頁
