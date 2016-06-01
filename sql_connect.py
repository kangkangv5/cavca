#encoding=utf-8
"""
Created on May 30
Author:kangkang
Function：
连接远程数据库。
192.168.1.222

暂用test_singers库作为测试。

数据库格式：
10001, "胡彦斌", "", "", null, "/6d/5f/f0f348cf461a2d6ecc288872c224.jpg", 1, 1, "HYB", 1, null, null, null, null, null, null, null, null, 207

接口txt格式：
90880|许嘉文|1|6|XJW|XU_JIA_WEN|null|男|414|1|3|
"""
import sys
import MySQLdb as mdb
import os
import codecs
import json
 
reload(sys)
sys.setdefaultencoding('utf-8')
 
conn = None
 
try:
    conn =  mdb.connect(host = '192.168.1.222',user = 'root',passwd='admin_root',db='KTVCenter',port=3306,charset='utf8')
    print 'connect done'
    cur = conn.cursor()
    cur.execute("select SingerName,SingerType,SingerSex,SingerArea from test_singers;")
    origin_singers = cur.fetchall()
    print origin_singers[:10]
    print 'fetch done'
    Singer_base_path = os.path.split(os.path.realpath(__file__))[0]+os.sep+'singer_base.txt'
    with codecs.open(Singer_base_path,'w')as f:
        for singer in origin_singers:
            json.dump(singer[0], f,ensure_ascii = False)
            f.write(',')
            json.dump(singer[1], f,ensure_ascii = False)
            f.write(',')
            json.dump(singer[2], f,ensure_ascii = False)
            f.write(',')
            json.dump(singer[3], f,ensure_ascii = False)
            
            f.write('\n')
    print 'write done'

finally:
    if conn:
        conn.close()

#数据对比

