#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Author  :   Allen
 
@License :   (C) Copyright 2018, Allen's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   Translate_Txt.py
 
@Time    :   June 21,2018
 
@Desc    :   此模块实现.txt文档的翻译功能.
 
'''


from TranslateBase import Translate
from Logger import Logger
from Translate_Func import *
import os


class TxtTranslate(Translate):
    
    def __init__(self, fileName,path):
        '''构造函数 path为文件绝对路径'''

        self.fileName = fileName
        self.path = path
        self.prepare()


    def translate(self):
        '''翻译txt文档'''

        '''流程：start->提取->翻译->写入->finish'''

        f = open(self.path)
        line = f.readline()
        temp_line = ''   # 拼接行
        
        while line:
            # 如果当前读取的行以回车结尾，那就拿这一段进行翻译，并写入翻译后的文件
            # 如果当前读取的行不是以回车结尾，则继续拼接文本
            if line.endswith('\n'):
                temp_line += line

                trans = baidu_translate(temp_line)
                self.write(temp_line)
                self.write(trans)

                temp_line = ''
            else:  # 实际上readline()就是读取一段文本，而不是表面上的一行
                temp_line += line

            line = f.readline()

        f.close()


    def prepare(self):
        '''准备：生成的文件名和路径'''

        # 查看要生成的文件名是否已存在，若存在，则在文件名中 + 1
        path = self.get_path('Doc_Out',self.fileName)
        i = 1
        file_name = ''

        while os.path.exists(path):   # 循环，生成新的文件名
            file_name = os.path.splitext(self.fileName)[0] + str(i) + '.txt'
            path = self.get_path('Doc_Out',file_name)
            i = i + 1

        self.new_path = path
        self.new_fileName = file_name


    def get_path(self,*paths):  # 如果这里的参数没有self的话，paths里将会包含这个类实例化对象，导致join方法出错
        '''获取，组装路径，参考os.path.join()方法实现'''

        path = os.path.split(os.path.realpath(__file__))[0]
        if len(paths):
            for i in range(len(paths)):
                path = os.path.join(path,paths[i])

        return path
    

    def write(self,content):
        '''写入文件'''

        # ‘a+’表示追加文本
        with open(self.new_path,'a+') as f:
            f.write(content)