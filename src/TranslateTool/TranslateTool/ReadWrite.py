#!/usr/bin/env python
# -*- encoding: utf-8 -*-
 
'''
@Author  :   Alen
 
@License :   (C) Copyright 2018, Allen's Studio
 
@Contact :   188512936@qq.com
 
@Software:   NaN
 
@File    :   ReadWrite.py
 
@Time    :   June 20,2018
 
@Desc    :   This module defines and implements read and write operations for TXT, Word, and PDF documents.
 
'''


import os


class ReadWriteBase(object):
    '''读写文档基类'''

    def Read(path):
        pass

    
    def Write(path,content):
        pass


class ReadWriteTXT(ReadWriteBase):
    '''读取TXT文档的实现类'''

    def Read(self,path):
        '''实现TXT文档的读取，一次将内容全部取出'''

        content = ''
        with open(path) as f:
            content = f.read()
        return content

    
    def Write(self,path,content):
        '''实现TXT文档的写方法'''

        with open(path,'a+') as f:
            f.write(content)


class ReadWriteWord(ReadWriteBase):
    '''读取Word文档的实现类'''

    def Read(path):
        pass


    def Write(path,content):
        pass


class ReadWritePDF(ReadWriteBase):
    '''读取PDF文档的实现类'''

    def Read(path):
        pass


    def Write(path,content):
        pass

