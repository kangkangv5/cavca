#coding:utf-8

"""
尝试获取新歌手。（对比base 和info的文件）
"""

import codecs
import pandas as pd
import time
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

base_data = pd.read_csv('E:/code/cavca/singer_base_test.txt',header=None)
cols = ['SingerName','SingerType','SingerSex','SingerArea']
base_data.columns=cols
print base_data[:5]
################################

data = pd.read_csv('E:/code/cavca/singer_info.txt',sep = '|',header=None)
cols = [ 'ID','SingerName','SingerType','歌手的首字笔画数','SingerPinyin','歌手全拼','SingerAnatherName','SingerSex','歌手笔画','SingerArea','歌手字数','NaN',]
data.columns=cols
#data为原始数据
#替换男女合唱组合为 1,2,3,4 ，和数据库的值同步。
data['SingerSex'] = data['SingerSex'].replace(['男','女','合唱','组合'],[1,2,3,4])

singer2 = data.iloc[:,[1,2,7,9]]
#print singer2[:5]


singer2['SingerType'] = singer2['SingerType'].replace([79,89,99,78,88,98,77,87,97,76,86,96,75,85,95,74,84,94,73,83,93],
                                                      [1,2,3,4,5,6,4,5,6,7,8,9,10,11,12,10,11,12,13,13,13])
#print singer2[:20]

base_data= base_data.sort(columns="SingerName")
df1=base_data.reindex()
singer2=singer2.sort(columns="SingerName")
df2=singer2.reindex()

df1['version']='old'
df2['version']='new'


full_set =pd.concat([df1,df2],ignore_index =True)
print len(full_set)
changes = full_set.drop_duplicates(subset = ['SingerName'],take_last=True)

print 'the all is %d' %len(changes)#两个的合集
print 'the new is %d' %len(df2)#新的歌手数据
print 'the base is %d' %len(df1)#基本歌手数据
#所以新加的数据应该是合集里有的而基本歌手里没有的

#获得所有出现过重复
dupe_accts = changes.set_index('SingerName').index.get_duplicates()

print dupe_accts
