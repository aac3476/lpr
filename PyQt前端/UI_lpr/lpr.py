from UI_lpr.car_idd import *
import UI_lpr.gl_headers
from hyperlpr import *
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy
from queue import Queue
import re
import requests
import json
import base64
from PyQt5.QtWidgets import *
import threading,time,os
from PyQt5.QtCore import QTimer


carre = "^(京[A-HJ-NPQY]|沪[A-HJ-N]|津[A-HJ-NPQR]|渝[A-DFGHN]|冀[A-HJRST]|晋[A-FHJ-M]|蒙[A-HJKLM]|辽[A-HJ-NP]|吉[A-HJK]|黑[A-HJ-NPR]|苏[A-HJ-N]|浙[A-HJKL]|皖[A-HJ-NP-S]|闽[A-HJK]|赣[A-HJKLMS]|鲁[A-HJ-NP-SUVWY]|豫[A-HJ-NP-SU]|鄂[A-HJ-NP-S]|湘[A-HJ-NSU]|粤[A-HJ-NP-Y]|桂[A-HJ-NPR]|琼[A-F]|川[A-HJ-MQ-Z]|贵[A-HJ]|云[AC-HJ-NP-SV]|藏[A-HJ]|陕[A-HJKV]|甘[A-HJ-NP]|青[A-H]|宁[A-E]|新[A-HJ-NP-S])([0-9A-HJ-NP-Z]{4}[0-9A-HJ-NP-Z挂试]|[0-9]{4}学|[A-D0-9][0-9]{3}警|[DF][0-9A-HJ-NP-Z][0-9]{4}|[0-9]{5}[DF])$|^WJ[京沪津渝冀晋蒙辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新]?[0-9]{4}[0-9JBXTHSD]$|^(V[A-GKMORTV]|K[A-HJ-NORUZ]|H[A-GLOR]|[BCGJLNS][A-DKMNORVY]|G[JS])[0-9]{5}$|^[0-9]{6}使$|^([沪粤川渝辽云桂鄂湘陕藏黑]A|闽D|鲁B|蒙[AEH])[0-9]{4}领$|^粤Z[0-9A-HJ-NP-Z][0-9]{3}[港澳]$"
#↑用来校验车牌的正则表达式

carpailist=[]#存最近识别的100个车牌的手动实现的队列，在队列中查找每个结果确保单个车牌不被多次触发
datalist = Queue()
num=0

def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, numpy.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontText)
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)

class lprclass:
    def __init__(self):
        self.running=True


    def carp(self):
        global carpailist,datalist
        global num
        cap = cv2.VideoCapture(0)
        while (cap.isOpened() and self.running):
            ret_flag, image = cap.read()

            r = 1000.0 / image.shape[1]
            dim = (1000, int(image.shape[0] * r))

            res = HyperLPR_PlateRecogntion(image)

            color = (255, 0, 0)
            for x in res:  # 遍历多个结果
                if re.match(carre, x[0]):  # 对识别出来的车牌进行正则校验，判断是否符合车牌格式
                    if x[0] in carpailist:
                        pass  # 这个车牌已经被触发过以此，直接跳过
                    else:
                        if len(carpailist) < 100:
                            carpailist.append(x[0])
                        else:
                            carpailist.pop(0)
                            carpailist.append(x[0])
                        print(x[0])
                        cv2.imwrite(r'./pic/' +str(num) + '.jpg', image)
                        data = {
                            'id': num,
                            'car': x[0],
                            'pre': x[1],
                            'pos_l': (x[2][0], x[2][1]),
                            'pos_r': (x[2][2], x[2][3])
                        }
                        UI_lpr.gl_headers.PICNUM=num
                        datalist.put(data)
                        num = num + 1
                        '''
                        这里添加其他代码，用于把识别后的结果返回给主窗口，识别后的参数在上面，可以直接调用，注意线程安全
                        '''
                        UI_lpr.gl_headers.CNUM = str(x[0])
                        


                    cv2.rectangle(image, (x[2][0], x[2][1]), (x[2][2], x[2][3]), color, 10)  # 第二三个参数为左上和右下坐标
                    image = cv2ImgAddText(image, x[0], x[2][0], x[2][3] + 20, color, 100)  # x[0]是识别到的车牌号
                    image = cv2ImgAddText(image, str(round(x[1] * 100, 2)) + "%", x[2][0], x[2][1] - 50, color,
                                          50)  # x[1]是置信度

            cv2.imshow("Capture_Test", image)  # 窗口显示，显示名为 Capture_Test


            k = cv2.waitKey(1) & 0xFF  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
            if k == ord('s'):  # 若检测到按键 ‘s’，打印字符串
                print(cap.get(3))
                print(cap.get(4))

            elif k == ord('q'):  # 若检测到按键 ‘q’，退出
                break

        cap.release()  # 释放摄像头
        cv2.destroyAllWindows()  # 删除opencv建立的全部窗口


    def down(self):
        self.running=False


    
