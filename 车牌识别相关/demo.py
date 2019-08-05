# -*- coding: utf-8 -*-  
"""
Create on 08-05 13:47 2019
@Author ywx 
@File demo.py
"""

from lpr import datalist,lprclass
import threading,time,os

def lpr():
    if datalist.empty():
        #没有数据进入，处理别的事情
        pass
    else:
        data=datalist.get(block=True, timeout=None)
        print(data)
        #这里接收数据，图片从pic/data['id'].jpg读取，用完之后记得删除
        # os.unlink('pic/'+str(data['id']+'.jpg')


ctl = lprclass()
thr = threading.Thread(target=ctl.carp)
thr.start()
while True:
    lpr()#这个地方不要用while True ，用pyqt的QTimer
    time.sleep(1)
