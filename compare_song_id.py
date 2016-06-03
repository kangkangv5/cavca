#encoding=utf-8

import sys
import MySQLdb as mdb
import os
import codecs
import json
import pandas as pd 
#from sql_connect import get_songs_info


def read_web_songs_another():
    web_song_id = pd.read_csv('E:/code/cavca/base_music.txt',usecols = [0,1],sep = '|',header=None)
    cols = ['SongId','SongName']
    web_song_id.columns= cols
    return web_song_id

def read_db_songs_another():
	base_songs_id = pd.read_csv('E:/code/cavca/base_compare.txt',sep = '|',header=None)
	cols = ['SongId','SongName']
	base_songs_id.columns= cols
	return base_songs_id


base_songs_id =read_db_songs_another()
web_songs_id = read_web_songs_another()

web_songs_id['SongId']  = web_songs_id['SongId'].map(lambda x:x.strip("mkv"))