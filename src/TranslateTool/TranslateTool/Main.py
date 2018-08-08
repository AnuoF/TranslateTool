#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Allen
 
@License :   (C) Copyright 2018, Allen's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   Main.py
 
@Time    :   June 21,2018
 
@Desc    :   程序入口模块.
 
'''


import os
from Logger import *
from T_Txt import TxtTranslate
from T_Pdf_pdfminer import PdfTranslate
from T_Docx import DocxTranslate
from T_Pdf_PyPDF2 import PdfTranslagePyPDF2


def run():

     # 提取档
    fileList = get_doc()
    if not fileList:
        # 文件不存在
        write_log('指定路径文件不存在，不执行翻译，结束程序。')
        return

    msg = '提取到 ' + str(len(fileList)) + ' 个文档'
    write_log(msg)

    # 创建文件夹（文档输出目录）
    if not os.path.exists(get_path('Doc_Out')):
        os.makedirs(get_path('Doc_Out'))

    for i in range(len(fileList)):
        doc = fileList[i]
        write_log('开始翻译' + doc)
        # 翻译单个文档
        translate_doc(doc)

    write_log('翻译完成，请查看Doc_Out文件夹下面的文档')


def translate_doc(doc):
    '''翻译单个文档'''

    path = get_path('Doc_In',doc)
    translate = get_translate(doc,path)
    if not translate:
        write_log('根据文件' + doc + '映射翻译对象失败！')
        return

    translate.translate()


def get_translate(doc,path):
    '''根据文件扩展名返回翻译对象'''

    tranlate = None
    extend_str = os.path.splitext(doc)[1]

    if extend_str == '.txt':
        tranlate = TxtTranslate(doc,path)
    elif extend_str == '.doc' or extend_str == '.docx':
        tranlate = DocxTranslate(doc,path)
    elif extend_str == '.pdf':
        #tranlate = PdfTranslagePyPDF2(doc,path)
        tranlate = PdfTranslate(doc,path)
    else:
        tranlate = None

    return tranlate


def get_doc():
    '''提取指定路径下的文件，返回文件列表'''

    path = get_path('Doc_In')
    if not os.path.exists(path):
        return None

    list = []
    dirs = os.listdir(path)
    for i in dirs:
        extend_str = os.path.splitext(i)[1]
        if extend_str == '.txt' or extend_str == '.pdf' or extend_str == '.doc' or extend_str == '.docx':
            list.append(i)

    return list


def get_path(*paths):
    '''获取、组装路径，参考os.path.join()方法实现'''

    path = os.path.split(os.path.realpath(__file__))[0]
    if len(paths):
        for i in range(len(paths)):
            path = os.path.join(path,paths[i])

    return path


def write_log(msg):
    '''打印消息并写日志'''

    # 写入日志文件
    Logger().write(msg)


# 启动时运行
if __name__ == '__main__':
    run()