#coding:utf-8
"""
Created on May 30
Author:kangkang
Function：
1、连接远程的接口。包括歌手，歌曲，新增歌曲，歌曲排行。
#TODO：和数据库比对，更新新增歌手到数据库。

服务器机器码：00:0E:C6:FA:E5:E8(目前在本地先直接给出。)
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
	#TODO
	songs_url = origin_url+'/music/mkvdatapackagelist'
	timestamp = time.time()
	md5target ="appid={0}&machinecode={1}&timestamp={2}&token={3}".format(appid,machinecode,timestamp,token)
	signature = hashlib.md5(md5target).hexdigest()
	params = {'appid':'yishang3682','machinecode':'00:0E:C6:FA:E5:E8','timestamp':str(timestamp),'signature':signature}
	request = rq.get(songs_url,params = params)
	songs_json = json.loads(request.content)
	try:

		delmusic_url =songs_json['packagelist'][0]['downloadurl']
		modify_url = songs_json['packagelist'][2]['downloadurl']
		base_url = songs_json['packagelist'][1]['downloadurl']
		
	except Exception:
		print "no music publish."

def new_songs():
	new_url = origin_url+'/music/newmusicdatapackagelist'
	timestamp = int(time.time())
	md5target ="appid={0}&machinecode={1}&timestamp={2}&token={3}".format(appid,machinecode,timestamp,token)
	signature = hashlib.md5(md5target).hexdigest()
	params = {'appid':'yishang3682','machinecode':'00:0E:C6:FA:E5:E8','timestamp':str(timestamp),'signature':signature}

	request = rq.get(new_url,params = params)
	new_json = json.loads(request.content)

	try:
		new_music = new_json['packagelist'][0]['downloadurl']
		print new_music
		req = rq.get(new_music)
		NewSongQath = os.path.split(os.path.realpath(__file__))[0]+os.sep+'new_music.txt'
		with codecs.open(NewSongQath,'w',encoding='utf-8')as f:
			f.write(req.content)
	except Exception:
		print "no new music publish."




new_songs()
