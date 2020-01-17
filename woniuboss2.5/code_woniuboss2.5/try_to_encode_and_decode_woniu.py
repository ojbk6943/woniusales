#!/usr/bin/env python
# -*- coding:utf-8 -*-
#====#====#====#====
# Author:
# CreateDate:
# Version:
#====#====#====#====


import jpype

jvmPath = jpype.getDefaultJVMPath()
print(jvmPath)
print(jpype.getClassPath())
jpype.startJVM(jvmPath, '-Djava.class.path=D:/woniuboss-decode.jar')
javaclass = jpype.JClass('com.woniuxy.des.DESede')
print(javaclass)
des = javaclass()
decode = des.decryptMode('35C50A9B463B93A3C034C0850DA6B091')
print(decode)
jpype.shutdownJVM()
#
# import hashlib
#
# m = hashlib.md5()
# m.update('woniu1234'.encode())
# print(m.digest())
# print(m.digest().hex())
# print(m.hexdigest())
# print(m.digest_size)

# import pyDes
#
# ptd = pyDes.triple_des(bytes(24), pyDes.CBC, b"\0\0\0\0\0\0\0\0",
#                  pad = None, padmode= pyDes.PAD_PKCS5)
# ed = ptd.encrypt("zhangfang放".encode('gbk'))
# print(ed.hex(), type(ed.hex()))
# print(ptd.decrypt(ed).decode('gbk'))
#
#
#
# print(ptd.decrypt(bytes.fromhex('9250bfb82211d3c730a34db7c9b7fd2c')).decode('gbk'))
# print(ptd.decrypt(bytes.fromhex('35C50A9B463B93A3C034C0850DA6B091')).decode('gbk'))
# print(ptd.decrypt(bytes.fromhex('411661DC12AC886B46D3B2165D309582')).decode('gbk'))







