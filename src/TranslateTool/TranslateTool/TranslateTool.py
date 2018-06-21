#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Allen
 
@License :   (C) Copyright 2018, Allen's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   TranslateTool.py
 
@Time    :   June 20,2018
 
@Desc    :   This module defines the main flow of the program.
 
'''


from Logger import *
from ReadWrite import *
import os
import Translate


def run():
    
    # 提取档
    fileList = get_doc()
    if not fileList:
        # 文件不存在
        print_write_msg('指定路径文件不存在，不执行翻译，结束程序。')
        return

    msg = '提取到 ' + str(len(fileList)) + ' 个文档'
    print_write_msg(msg)

    for i in range(len(fileList)):
        doc = fileList[i]
        print_write_msg('开始翻译' + doc)
        # 翻译单个文档
        translate_doc(doc)
        print_write_msg(doc + '翻译完成')

    print_write_msg('翻译完成，请查看Doc_Out文件夹下面的文档')


def translate_doc(doc):
    '''翻译单个文档'''
    
    read_write = get_readwrite(doc)
    if not read_write:
        print_write_msg('根据文件' + doc + '映射读写对象失败！')
        return

    path = get_path('Doc_In',doc)
    content = read_write.Read(path)
    trans = Translate.baidu_translate(content)
    path_out = get_path('Doc_Out',doc)

    if not os.path.exists(get_path('Doc_Out')):
        os.makedirs(get_path('Doc_Out'))

    read_write.Write(path_out,trans)


def get_doc():
    '''提取指定路径下的文件，返回文件列表'''

    #path = os.path.split(os.path.realpath(__file__))[0]
    #path = os.path.join(path,'Doc_In')

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
    '''获取，组装路径，参考os.path.join()方法实现'''

    path = os.path.split(os.path.realpath(__file__))[0]
    if len(paths):
        for i in range(len(paths)):
            path = os.path.join(path,paths[i])

    return path


def print_write_msg(msg):
    '''打印消息并写日志'''

    # 写入日志文件
    logger = Logger()
    logger.write(content)


def get_readwrite(doc):
    '''根据文件扩展名返回读写文件对象'''

    readwrite = None
    extend_str = os.path.splitext(doc)[1]

    if extend_str == '.txt':
        readwrite = ReadWriteTXT()
    elif extend_str == '.doc':
        readwrite = ReadWriteWord()
    elif extend_str == '.pdf':
        readwrite = ReadWritePDF()
    else:
        readwrite = None

    return readwrite


# 启动时运行
if __name__ == '__main__':
    run()

