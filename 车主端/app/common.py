# -*- coding: utf-8 -*-  
"""
Create on 04-26 19:09 2019
@Author ywx 
@File function.py
"""
from hashlib import md5
import hashlib
from random import Random
import re,os


def checkQQ(str):
    pattern = r"[1-9]\d{4,10}"
    res = re.findall(pattern, str, re.I)
    return len(res)


def create_salt(length=4):
    salt = ''
    chars = '0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in range(length):
        salt += chars[random.randint(0, len_chars)]
    return salt


def create_md5(pwd):
    md5_obj = md5()
    md5_obj.update(pwd.encode("utf8"))
    return md5_obj.hexdigest()


def checkemail(addr):
    re_email = re.compile(r'^[a-zA-Z\.]+@[a-zA-Z0-9]+\.[a-zA-Z]{3}$')
    return re_email.match(addr)


__supported_hashfunc = {'md5':hashlib.md5, 'sha1':hashlib.sha1, 'sha224':hashlib.sha224, 'sha256':hashlib.sha256, 'sha384':hashlib.sha384, 'sha512':hashlib.sha512}
__FILE_SLIM = (100*1024*1024) # 100MB

def filehash(hfunc,filename):
    hobj = hfunc()
    fp = open(filename,"rb")
    f_size = os.stat(filename).st_size
    while(f_size > __FILE_SLIM):
        hobj.update(fp.read(__FILE_SLIM))
        f_size /= __FILE_SLIM
        #print("o.o")
    if(f_size>0) and (f_size <= __FILE_SLIM):
            hobj.update(fp.read())
    fp.close()
    return hobj.hexdigest()

def paicheck(pai):
    carre = "^(京[A-HJ-NPQY]|沪[A-HJ-N]|津[A-HJ-NPQR]|渝[A-DFGHN]|冀[A-HJRST]|晋[A-FHJ-M]|蒙[A-HJKLM]|辽[A-HJ-NP]|吉[A-HJK]|黑[A-HJ-NPR]|苏[A-HJ-N]|浙[A-HJKL]|皖[A-HJ-NP-S]|闽[A-HJK]|赣[A-HJKLMS]|鲁[A-HJ-NP-SUVWY]|豫[A-HJ-NP-SU]|鄂[A-HJ-NP-S]|湘[A-HJ-NSU]|粤[A-HJ-NP-Y]|桂[A-HJ-NPR]|琼[A-F]|川[A-HJ-MQ-Z]|贵[A-HJ]|云[AC-HJ-NP-SV]|藏[A-HJ]|陕[A-HJKV]|甘[A-HJ-NP]|青[A-H]|宁[A-E]|新[A-HJ-NP-S])([0-9A-HJ-NP-Z]{4}[0-9A-HJ-NP-Z挂试]|[0-9]{4}学|[A-D0-9][0-9]{3}警|[DF][0-9A-HJ-NP-Z][0-9]{4}|[0-9]{5}[DF])$|^WJ[京沪津渝冀晋蒙辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新]?[0-9]{4}[0-9JBXTHSD]$|^(V[A-GKMORTV]|K[A-HJ-NORUZ]|H[A-GLOR]|[BCGJLNS][A-DKMNORVY]|G[JS])[0-9]{5}$|^[0-9]{6}使$|^([沪粤川渝辽云桂鄂湘陕藏黑]A|闽D|鲁B|蒙[AEH])[0-9]{4}领$|^粤Z[0-9A-HJ-NP-Z][0-9]{3}[港澳]$"
    if re.match(carre, pai):
        return True
    else:
        return False