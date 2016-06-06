#encoding=utf-8
"""
author:kang
date:2016.06.04~2016.06.06
说明：
寻找新的歌曲，方便后续的mkv下载。

歌曲的id是唯一的。
Id的提取：
数据库中：CONCAT('50',SUBSTR(SongfileName,4,6))
网络中：str.strip(‘ktv’) 


"""
import sys
import MySQLdb as mdb
import os
import codecs
import json
import pandas as pd 
#from sql_connect import get_songs_info

def read_web_songs():
	#获取网上base_music数据。replace替换值，是为了和数据库一致。
    web_songs = pd.read_csv('E:/code/cavca/base_music.txt',usecols = [1,23,20,24,25,14,19],sep = '|',header=None)
    cols = ['SongName','SongType','SongScreen','SongProperty','SongVersion','SongPublishArea','SongLanguage']
    web_songs.columns= cols
    web_songs['SongScreen'] = web_songs['SongScreen'].replace([7,5,2,1],[1,2,3,4])
    web_songs['SongLanguage'] = web_songs['SongLanguage'].replace([0,1,2,3,4,5,6],[1,2,4,3,5,6,7])
    return web_songs
def read_db_songs():
	#从数据库读取已有的歌曲信息。
    base_songs = pd.read_csv('E:/code/cavca/song_base_tb.txt',sep = '|',header=None)
    cols =['SongName','SongType','SongScreen','SongProperty','SongVersion','SongPublishArea','SongLanguage']
    base_songs.columns = cols
    return base_songs

def read_web_songs_another():
	#只用base_music的id和name
    web_songs_id = pd.read_csv('E:/code/cavca/base_music.txt',usecols = [0,1],sep = '|',header=None)
    cols = ['SongId','SongName']
    web_songs_id.columns= cols
    web_songs_id['version']='new'
    return web_songs_id

def read_db_songs_another():
	#只用数据库的id和name
	base_songs_id = pd.read_csv('E:/code/cavca/base_compare.txt',sep = '|',header=None)
	cols = ['SongId','SongName']
	base_songs_id.columns= cols
	base_songs_id['version']='old'
	return base_songs_id


base_songs_id =read_db_songs_another()
web_songs_id = read_web_songs_another()

base_songs_id['version']='old'
web_songs_id['version']='new'
web_songs_id['SongId']  = web_songs_id['SongId'].map(lambda x:x.strip("mkv"))
base_songs_id['SongId']  = base_songs_id['SongId'].map(lambda x:str(x))
#df['A'].str.extract('(\d*)')
#.map(lambda x:x[:-3],df['SongId'])也可

#print web_songs_id  类似于：135501  50101390  两个人的西洋棋     new

full_set =pd.concat([base_songs_id,web_songs_id],ignore_index =True)
#changes = full_set.drop_duplicates(subset = ['SongId'],take_last=True)
#去重，只留下new里面独有的。
grouped = full_set.groupby(['SongId'])
#print len(changes)
print len(web_songs_id)
print len(base_songs_id)
print len(grouped)
only_new = grouped.filter(lambda grouped:(grouped.shape[0] == 1 and grouped['version']=='new'))
print len(only_new)
only_new = only_new.drop(['version'],axis =1)

new_song_path = os.path.split(os.path.realpath(__file__))[0]+os.sep+'new_song_id.txt'
only_new.to_csv(new_song_path,columns = ['SongId','SongName'],header =None,index = False)
#only_new为只有新歌里面有的id。而老歌里面没有。

