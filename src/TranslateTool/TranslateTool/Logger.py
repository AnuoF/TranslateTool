#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Author  :   Allen
 
@License :   (C) Copyright 2018, Allen's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   log.py
 
@Time    :   June 20,2018
 
@Desc    :   This module implements log records and maintenance ,using singleton pattern.
 
'''

import os
import datetime


# 日志类
class Logger(object):
    '''实现日志的记录和维护，采用单例模式'''
    
    def __init__(self):
        '''初始化时删除先前的日志'''

        # 获取运行目录
        path = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(path,'log')
        if not os.path.exists(path):
            os.makedirs(path)

        self.log_path = os.path.join(path,'log.txt')


    def __new__(cls,*args,**kwargs):
        '''实现单例模式'''

        if not hasattr(Logger,"_instance"):
            Logger._instance = object.__new__(cls)
        return Logger._instance


    def write(self,content):
        '''写日志'''
        
         # 添加时间信息
        time_str = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
        content = '[' + time_str + '] -> ' + content + '\n'

        # 打印消息
        print(content)
        # 写文件
        with open(self.log_path,'a+',encoding='utf-8') as f:
            f.write(content)
    

    def delete_old_log():
        '''删除之前存在的日志文件'''
        
        # 获取运行目录
        path = os.path.split(os.path.realpath(__file__))[0]
        path = os.path.join(path,'log')

        if os.path.exists():
            os.path.removedirs(path)

        os.path.mkdir(path)
        log_path = os.path.join(path,'log.txt')
