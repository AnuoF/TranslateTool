#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Allen
 
@License :   (C) Copyright 2018, Allen's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   T_Pdf_PyPDF2.py
 
@Time    :   June 23,2018
 
@Desc    :   此模块实现.pdf文档的翻译功能，读取PDF文档，并将内容翻译，写入txt文档。
 
'''


import os
from TranslateFunc import *
from T_Base import Translate
from Logger import *
# 安装指令：pip install pypdf2
from PyPDF2.pdf import PdfFileReader

class PdfTranslagePyPDF2(Translate):
    '''PDF文档翻译模块'''

    def __init__(self, fileName, fullPath):
        '''构造函数'''
        # fileName:文件名
        # fullPath:全路径

        self.fileName = fileName
        self.fullPath = fullPath
        self.prepare()


    def translate(self):
        '''读取pdf内容，并翻译，写入txt文件'''
        f = open(self.fullPath,'rb')
        pdf = PdfFileReader(f)

        index = 0
        for i in range(0,pdf.getNumPages()):
            extractedText = pdf.getPage(i).extractText()
            content = extractedText.split('\n')  
            content = self.removeBlankFromList(content)  

            # 拼接之后的文本，如果单词间歇超过一个空格的，认为是需要换行处理的
            content_list = self.enter_symbol(content)

            for line in content_list:
                line = line.strip()
                if line:
                    ret = translate_func(line)
                    trans = ret if ret else '翻译失败'
                    self.write(line + '\n')
                    self.write(trans)
                    index += 1
                    print(index,end=' ',flush=True)

        f.close()
        Logger().write(self.fileName + '翻译完成，新文档：' + self.new_fullPath)


    def removeBlankFromList(self,list_old):
        '''移除空白'''

        list_new = []  
        for i in list_old:  
            if i != '':  
                list_new.append(i)  
        return self.combine_list2str(list_new)


    def combine_list2str(self,list_old):
        '''列表到字符串的转换'''

        s = ''
        for i in list_old:
            s += i
        return s


    def enter_symbol(self,content_old):
        '''换行处理，返回处理后的行列表'''
        
        content = content_old
        for i in range(10,1,-1):
            symbol = ' '
            symbol = symbol * i
            content = content.replace(symbol,'A34EN')
        return content.split('A34EN')


    def prepare(self):
        '''准备：生成的文件名和路径'''

        # 查看要生成的文件名是否已存在，若存在，则在文件名中 + 1
        file_name = os.path.splitext(self.fileName)[0] + '_pdf.txt'
        path = self.get_path('Doc_Out',file_name)
        i = 1

        while os.path.exists(path):   # 循环，生成新的文件名
            file_name = os.path.splitext(self.fileName)[0] + str(i) + '_pdf.txt'
            path = self.get_path('Doc_Out',file_name)
            i = i + 1

        self.new_fileName = file_name
        self.new_fullPath = path


    def get_path(self,*paths):
        '''获取，组装路径，参考os.path.join()方法实现'''

        path = os.path.split(os.path.realpath(__file__))[0]
        if len(paths):
            for i in range(len(paths)):
                path = os.path.join(path,paths[i])

        return path


    def write(self,content):
        '''写入文件'''

        #content = str(content.encode('utf-8'))
        # ‘a+’表示追加文本
        with open(self.new_fullPath,'a+',encoding='utf-8') as f:
            f.write(content)