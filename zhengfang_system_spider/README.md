# ZhengFang_System_Spider
對正方教務管理系統的個人課表，個人學生成績，績點等簡單爬取

## 依賴環境
python 3.6
### python庫
http請求：requests，urllib  
數據提取：re，lxml，bs4  
存儲相關：os，sys  
驗證碼處理：PIL  

## 下載安裝
在終端輸入如下命令：
```bash
git clone git@github.com:Jack-Cherish/python-spider.git
```

## 使用方法

### 安裝依賴包
```bash
pip install -r requirements.txt
```

### 運行
在當前目錄下輸入：
```
cd zhengfang_system_spider
python spider.py
```
運行爬蟲，按提示輸入學校教務網，學號，密碼，輸入驗證碼  

![運行時](/zhengfang_system_spider/screenshot/spider.png)

稍等幾秒鐘，當前ZhengFang_System_Spider文件夾下就會生成zhengfang.txt  
個人課表，成績績點均已保存到該文本文件中

![結果](/zhengfang_system_spider/screenshot/zf.png)
