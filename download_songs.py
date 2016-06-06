#coding:utf-8
"""
author：kang
date：2016.06.06
根据下载链接，下载歌曲。
测试OK

根据文档，下载完毕之后，调用下载完成接口。(需要tkid)

#TODO:如果下载出现问题，调用problem.怎么判断出现问题了呢？
暂时定为下载失败，raise错误吧。
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

def get_song_list():
	DownLoadQath = os.path.split(os.path.realpath(__file__))[0]+os.sep+'download_song_urls.txt'
	song_list = []
	with open(DownLoadQath,'r')as f:
		for data in f.readlines():
			song_list.append(data.split(','))

	return song_list


def download_song(url,tkid):
	#下载歌曲暂时到本地-->可能会改变目标保存位置。
	#歌曲名为id名。
	song = rq.get(url,stream = True)
	song_name = url[24:36]
	#print song.status_code
	DownLoadQath = os.path.split(os.path.realpath(__file__))[0]+os.sep+song_name
	try:
		with open(DownLoadQath,'wb')as f:
			for chunk in song.iter_content(500): #设定保存的字节量。防止内存过大。
				f.write(chunk)
		print "download done"
		callback_status(tkid)
	except Exception:
		problem_feedback(tkid)


#download_song('http://source.cavca.net/50539858.mkv?e=1465212572&token=Bn_T1dBEDofdD-StJcNT-ewNbDod3fmHtqwzg4K5:gvRaK0wsTi4hogjTq9hJ43P6PHw=')


def callback_status(tkid):
	#下载结束后调用函数，更新状态给平台。
	origin_url ="http://www.cavca.net"
	appid = "yishang3682"
	machinecode="00:0E:C6:FA:E5:E8"
	token = "60159105e8374c21a28ca117738b2761"
	timestamp = int(time.time())
	finish_url = origin_url+'/music/finishdownload'
	md5target ="appid={0}&machinecode={1}&timestamp={2}&tkid={3}&token={4}".format(appid,machinecode,str(timestamp),tkid,token)
	signature = hashlib.md5(md5target).hexdigest()
	params = {'appid':'yishang3682','machinecode':'00:0E:C6:FA:E5:E8','timestamp':str(timestamp),'tkid':tkid,'signature':signature}
	request = rq.get(finish_url,params = params)
	status_json = json.loads(request.content)
	try:
		result = status_json['result']
		print result  #正常为1标志，标识下载状态更新完毕。测试成功。
	except Exception:
		print result
		print "status update unsecuess"


def problem_feedback(tkid):
	#如果无法下载时，调用此函数，告知平台。
	origin_url ="http://www.cavca.net"
	appid = "yishang3682"
	machinecode="00:0E:C6:FA:E5:E8"
	token = "60159105e8374c21a28ca117738b2761"
	timestamp = int(time.time())
	del_url = origin_url+'/music/finishdownload'
	md5target ="appid={0}&machinecode={1}&timestamp={2}&tkid={3}&token={4}".format(appid,machinecode,str(timestamp),tkid,token)
	signature = hashlib.md5(md5target).hexdigest()
	params = {'appid':'yishang3682','machinecode':'00:0E:C6:FA:E5:E8','timestamp':str(timestamp),'tkid':tkid,'signature':signature}
	request = rq.get(del_url,params = params)
	status_json = json.loads(request.content)
	try:
		result = status_json['result']
		print result
	except Exception:
		print result
		print "problem status update unsecuess"


if __name__ == '__main__':
	song_list= get_song_list()

	for song in song_list:
		download_song(song[0],song[1])
		

#download_song('http://source.cavca.net/50539937.mkv?e=1465218576&token=Bn_T1dBEDofdD-StJcNT-ewNbDod3fmHtqwzg4K5:nQxSBfMAyTecy_CUVJWZ9JeJYOg=','fedc69f9a3a84bffb0a17e841c147ac6')
