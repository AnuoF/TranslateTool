#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Allen
 
@License :   (C) Copyright 2018, Allen's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   T_Pdf_pdfminer.py
 
@Time    :   June 21,2018
 
@Desc    :   此模块实现.pdf文档的翻译功能，读取PDF文档，并将内容翻译，写入txt文档。
 
'''


from T_Base import Translate
from Logger import *
from TranslateFunc import *
import os
import time

# 安装指令：pip install PyExecJS
from pdfminer.pdfparser import PDFParser,PDFDocument   # pip install pdfminer3k
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.layout import LAParams,LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


class PdfTranslate(Translate):
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

        # 以二进制读模式打开本地pdf文件
        fp = open(self.fullPath,'rb')
        # 用文件对象来创建一个pdf文档分析器
        praser_pdf = PDFParser(fp)
        # 创建一个PDF文档
        doc_pdf = PDFDocument()
        # 连接分析器与文档对象
        praser_pdf.set_document(doc_pdf)
        doc_pdf.set_parser(praser_pdf)
        # 提供初始化密码doc.initialize("123456")，如果没有密码 就创建一个空的字符串
        doc_pdf.initialize()

        # 检查文档是否提供txt转换，不提供就无法翻译文档
        if not doc_pdf.is_extractable:
            Logger().write(self.fileName + '未能提取有效的文本，停止翻译。')
            return
        else:
            # 创建PDF资源管理器来共享资源
            rsrcmgr = PDFResourceManager()
            # 创建一个PDF参数分析器
            laparams = LAParams()
            # 创建聚合器
            device = PDFPageAggregator(rsrcmgr,laparams=laparams)
            # 创建一个PDF页面解释器对象
            interpreter = PDFPageInterpreter(rsrcmgr,device)

            i = 0
            # 循环遍历列表，每次处理一页的内容
            for page in doc_pdf.get_pages():
                # 使用页面解释器来读取
                interpreter.process_page(page)
                # 使用聚合器获取内容
                layout = device.get_result()

                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                for out in layout:
                    # 判断是否含有get_text()方法，图片之类的就没有
                    if isinstance(out,LTTextBoxHorizontal):
                        content = out.get_text().strip()
                        if content:
                            to_trans_content = content.replace("\r\n","")
                            ret = translate_func(to_trans_content)
                            trans = ret if ret else '翻译失败'

                            self.write(content)
                            self.write(trans)
                            i += 1
                            print(i,end=' ',flush=True)

                time.sleep(2);

            Logger().write(self.fileName + '翻译完成，新文档：' + self.new_fullPath)


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

        # https://www.cnblogs.com/themost/p/6603409.html
        # ‘a+’表示追加文本，txt文本打开默认是gbk编码，需要设置成utf-8
        with open(self.new_fullPath,'a+',encoding='utf-8') as f:
            f.write(content)