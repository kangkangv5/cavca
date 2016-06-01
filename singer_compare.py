# -*-coding:utf8 -*-
"""
Created on May 31
Author:kangkang
Function：
比较新歌手数据中更新的部分，加入数据库.
"""
import json
import pandas as pd 
import sys
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')

def singerType(test):#映射到和SQL一致。
	for t in test.values:
	    if t[7]=='男':
	        t[7] = t[7].replace('男','1')
	    elif t[7]=='女':
	        t[7] = t[7].replace('女','2')
	    elif t[7]=='合唱':
	        t[7] = t[7].replace('合唱','3')
	    elif t[7]=='组合':
	        t[7] = t[7].replace('组合','4')	
	    print t
	return test
	

def compare(new,base):
	"""
	new = []
	base = []
	"""
	BaseSet = set(base)
	new_name = []
	for name in new:
	    if name not in BaseSet:
	        new_name.append(name)
	return new_name

def singers_web():
	#读取网上下载的数据new
	data = pd.read_csv('E:/code/cavca/singer_info.txt',sep = '|',header=None)
	cols = [ 'ID','SingerName','SingerType','歌手的首字笔画数','SingerPinyin','歌手全拼','SingerAnatherName','SingerSex','歌手笔画','SingerArea','歌手字数','NaN',]
	data.columns=cols
	#data为原始数据
	#替换男女合唱组合为 1,2,3,4 ，和数据库的值同步。
	data['SingerSex'] = data['SingerSex'].replace(['男','女','合唱','组合'],[1,2,3,4])
	singer2 = data.iloc[:,[1,2,7,9]]
	new = [t[0] for t in singer2.values]
	return new,data


def singers_base():
	#读取数据库的基本数据：base
	base_data = pd.read_csv('E:/code/cavca/singer_base_test.txt',header=None)
	cols = ['SingerName','SingerType','SingerSex','SingerArea']
	base_data.columns=cols
	base= [t[0] for t in base_data.values]
	return base




def insert_singers(new_name):
	#新歌手加入数据库
	conn = None
	max_Id_sql ="SELECT MAX(SingerId) FROM `KTVCenter`.`test_singers`;"

	try:
		conn =  mdb.connect(host = '192.168.1.222',user = 'root',passwd='admin_root',db='KTVCenter',port=3306,charset='utf8')
		print 'connect done'
		cur = conn.cursor()
		cur.execute(max_Id_sql)
		max_id =int(cur.fetchone()[0])#34044S
		id_old = max_id

		for new in new_name:
			new_info = data[data['SingerName'] ==new]
			#print new_info
			update_sql = """
	    	INSERT INTO `KTVCenter`.`test_singers`
							(`SingerId`,
							`SingerName`,
							`SingerAnatherName`,
							`SingerType`,
							`SingerArea`,
							`SingerPinyin`,
							`SingerSex`)VALUES({0},"{1}","{2}",{3},{4},"{5}",{6});
	""".format(max_id,str(new_info['SingerName'].values[0]),new_info['SingerAnatherName'].values[0],new_info['SingerType'].values[0],new_info['SingerArea'].values[0],new_info['SingerPinyin'].values[0],new_info['SingerSex'].values[0])
			

			#print update_sql
			cur.execute(update_sql)
			conn.commit()
			max_id+=1

	finally:
	    if conn:
	        conn.close()
	        print "{} singers update.".format(str(max_id-id_old))


if __name__ == '__main__':
	new,data = singers_web()
	base = singers_base()
	#新增名字到new_name  []
	new_name = compare(new,base)
	insert_singers(new_name)

