#coding:utf-8
"""
Created on May 30
Author:kangkang
Function：
1、连接远程的接口。包括歌手，歌曲，新增歌曲，歌曲排行。

服务器机器码：00:0E:C6:FA:E5:E8(目前在本地先直接给出。可自行识别)
token = "60159105e8374c21a28ca117738b2761"  暂时没发现变化
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



def cloud_get():
	machine_url = origin_url+"/machine/assotagcode"
	timestamp = int(time.time())
	md5target ="appid={0}&machinecode={1}&timestamp={2}&token={3}".format(appid,machinecode,str(timestamp),token)
	signature = hashlib.md5(md5target).hexdigest()
	params = {'appid':'yishang3682','machinecode':'00:0E:C6:FA:E5:E8','timestamp':str(timestamp),'signature':signature}

	request = rq.get(machine_url,params = params)
	print request.text
	print request.url

def singers_info():
	#下载歌手信息
	singer_url = origin_url+'/music/singerdatapackage'
	timestamp = time.time()
	md5target ="appid={0}&machinecode={1}&timestamp={2}&token={3}".format(appid,machinecode,timestamp,token)
	signature = hashlib.md5(md5target).hexdigest()
	params = {'appid':'yishang3682','machinecode':'00:0E:C6:FA:E5:E8','timestamp':str(timestamp),'signature':signature}
	request = rq.get(singer_url,params = params)
	singer_json = json.loads(request.content)
	try:
		singer_download=singer_json['downloadurl']
		req = rq.get(singer_download)
		SingerQath = os.path.split(os.path.realpath(__file__))[0]+os.sep+'singer_info.txt'
		with codecs.open(SingerQath,'w',encoding='utf-8')as f:
			f.write(req.content)
	except Exception:
		print "no singers.procedure breaks"
	

def songs_info():
	#TODO 下载歌曲信息，包括基本歌曲，（删除歌曲，修改歌曲先不用下载）
	songs_url = origin_url+'/music/mkvdatapackagelist'
	timestamp = time.time()
	md5target ="appid={0}&machinecode={1}&timestamp={2}&token={3}".format(appid,machinecode,timestamp,token)
	signature = hashlib.md5(md5target).hexdigest()
	params = {'appid':'yishang3682','machinecode':'00:0E:C6:FA:E5:E8','timestamp':str(timestamp),'signature':signature}
	request = rq.get(songs_url,params = params)
	songs_json = json.loads(request.content)
	print songs_json

	#base music
	try:
		base_url = songs_json['packagelist'][1]['downloadurl']
		print base_url
		req = rq.get(base_url,stream= True)
		BasePath = os.path.split(os.path.realpath(__file__))[0]+os.sep+'base_music.txt'
		with codecs.open(BasePath,'w',encoding='utf-8')as f:
			for data in req.iter_lines():
				f.write(data)
				f.write('\n')
		print "write music done"
	except Exception:
		print "no music publish."

def new_songs():
	#新歌信息
	new_url = origin_url+'/music/newmusicdatapackagelist'
	timestamp = int(time.time())
	md5target ="appid={0}&machinecode={1}&timestamp={2}&token={3}".format(appid,machinecode,timestamp,token)
	signature = hashlib.md5(md5target).hexdigest()
	params = {'appid':'yishang3682','machinecode':'00:0E:C6:FA:E5:E8','timestamp':str(timestamp),'signature':signature}

	request = rq.get(new_url,params = params)
	new_json = json.loads(request.content)

	try:
		print new_json
		new_music = new_json['packagelist'][0]['downloadurl']

		req = rq.get(new_music)
		NewSongQath = os.path.split(os.path.realpath(__file__))[0]+os.sep+'new_music.txt'
		with codecs.open(NewSongQath,'w',encoding='utf-8')as f:
			f.write(req.content)
	except Exception:
		print "no new music publish."




songs_info()
