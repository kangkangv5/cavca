#coding:utf-8
"""
根据新增的歌曲ID（主键），获取下载地址的url。

/music/finishdownload?
应用id（已知）：appid=boosoo&
机器码（已知）：machinecode=60:A7:4C:B4:96:E9&
时间戳：timestamp=1449054011&
歌曲标识：tidcode=50546465mkv
加密字符（md5）：signature=410482d8d80861266e71456ffc6f8e13
"""
import sys
import requests as rq 
import time
import hashlib
import json
import os
import codecs 


reload(sys)
sys.setdefaultencoding('utf-8')


origin_url ="http://www.cavca.net"
appid = "yishang3682"
machinecode="00:0E:C6:FA:E5:E8"
token = "60159105e8374c21a28ca117738b2761"


#将下载的链接保存在download_song_urls.txt中。tidcode是下载歌曲标识。
def save_urls(tidcode):
	down_url = origin_url+'/music/begindownload'
	timestamp = int(time.time())
	md5target ="appid={0}&machinecode={1}&timestamp={2}&tidcode={3}&token={4}".format(appid,machinecode,str(timestamp),tidcode,token)
	signature = hashlib.md5(md5target).hexdigest()
	params = {'appid':'yishang3682','machinecode':'00:0E:C6:FA:E5:E8','timestamp':str(timestamp),'tidcode':tidcode,'signature':signature}
	download_url=down_url+"?appid={0}&machinecode={1}&timestamp={2}&tidcode={3}&signature={4}".format(appid,machinecode,str(timestamp),tidcode,signature)

	request = rq.get(download_url)
	#print request.text
	download_json = json.loads(request.content)
	try:
		mkv_download=download_json['downloadurl']
		DownLoadQath = os.path.split(os.path.realpath(__file__))[0]+os.sep+'download_song_urls.txt'
		with open(DownLoadQath,'a+')as f:
			f.write(mkv_download)
			f.write('\n')
	except Exception:
		print download_json
		print "no url exists.you can try yourself "


#save_urls('50539858mkv')
def get_tidcode_list():
	tidcode_list = []
	with open(os.path.split(os.path.realpath(__file__))[0]+os.sep+'new_song_id.txt','r')as f:
		for one in f.readlines():
			tidcode_list.append(one.split(','))
	tid = []
	for data in tidcode_list:
		tid.append(data[0]+'mkv')
	return tid  #获取tidcode列表。



if __name__ == '__main__':
	tidcode_list = get_tidcode_list()
	for tidcode in tidcode_list:
		save_urls(tidcode)
		#列表1600个新的tidnode，需要获取每个download_url的时间约为0.2~0.5s
		#所以总共需要9~15分钟。

