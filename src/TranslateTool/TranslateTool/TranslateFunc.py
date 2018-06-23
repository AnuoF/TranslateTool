#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Author  :   Allen
 
@License :   (C) Copyright 2018, Allen's Studio
 
@Contact :   188512936@qq.com
 
@Software:   VS2017
 
@File    :   Translate_Func.py
 
@Time    :   June 21,2018
 
@Desc    :   实现翻译的爬虫功能.
 
'''

import urllib.request
import urllib.parse
import json
import requests
from Py4Js import *


#class TranslateFunc(object):

#    def __new__(cls,*args,**kwargs):
#        '''实现单例模式'''

#        if not hasattr(TranslateFunc,'_instance'):
#            TranslateFunc._instance = object.__new__(cls)
#        return TranslateFunc._instance


#    def get_translate_func(self,type):
#        '''根据类型选择翻译接口'''

#        if type == 'baidu':
#            return self.baidu_translate
#        elif type == 'google':
#            return self.google_translate
#        else:
#            return self.youdao_translate


# 百度翻译方法
def baidu_translate(content,type=1):
    '''实现百度翻译'''

    baidu_url = 'http://fanyi.baidu.com/basetrans'
    data = {}

    data['from'] = 'en'
    data['to'] = 'zh'
    data['query'] = content
    data['transtype'] = 'translang'
    data['simple_means_flag'] = '3'
    data['sign'] = '94582.365127'
    data['token'] = 'ec980ef090b173ebdff2eea5ffd9a778'
    data = urllib.parse.urlencode(data).encode('utf-8')

    headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}
    baidu_re = urllib.request.Request(baidu_url, data, headers)
    baidu_response = urllib.request.urlopen(baidu_re)
    baidu_html = baidu_response.read().decode('utf-8')
    target2 = json.loads(baidu_html)

    trans = target2['trans']
    ret = ''
    for i in range(len(trans)):
        ret += trans[i]['dst'] + '\n'

    return ret


# 有道翻译方法
def youdao_translate(content):
    '''实现有道翻译的接口'''

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=https://www.baidu.com/link'
    data = {
        'from':'AUTO',
        'to':'AUTO',
        'smartresult':'dict',
        'client':'fanyideskweb',
        'salt':'1500092479607',
        'sign':'d9f9a3aa0a7b34241b3fe30505e5d436',
        'doctype':'json',
        'version':'2.1',
        'keyfrom':'fanyi.web',
        'action':'FY_BY_CL1CKBUTTON',
        'typoResult':'true'}

    data['i'] = content

    data = urllib.parse.urlencode(data).encode('utf-8')
    wy = urllib.request.urlopen(url,data)
    html = wy.read().decode('utf-8')

    ta = json.loads(html)
    return ta['translateResult'][0][0]['tgt']

    # 下面的代码不能使用
    youdao_url = 'http://fanyi.youdao.com/translate'  
    data = {}
    
    data['i']= content
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['salt'] = '1525141473246'
    data['sign'] = 'd9f9a3aa0a7b34241b3fe30505e5d436'
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CLICKBUTTION'
    data['typoResult'] = 'false'
    data = urllib.parse.urlencode(data).encode('utf-8')

    youdao_response = urllib.request.urlopen(youdao_url, data)
    youdao_html = youdao_response.read().decode('utf-8')
    target = json.loads(youdao_html)

    trans = target['translateResult']
    ret = ''
    for i in range(len(trans)):
        line = ''
        for j in range(len(trans[i])):
            line = trans[i][j]['tgt']
        ret += line + '\n'

    return ret


# 谷歌翻译方法
def google_translate(content):
    '''实现谷歌的翻译'''

    js = Py4Js()
    tk = js.getTk(content)

    if len(content) > 4891:      
        print("翻译的长度超过限制！！！")      
        return ''   
  
    param = {'tk': tk, 'q': content}  
  
    result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=en 
        &tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss 
        &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)  
  
    #返回的结果为Json，解析为一个嵌套列表  
    trans = result.json()[0]
    ret = ''
    for i in range(len(trans)):
        line = trans[i][0]
        if line != None:
            ret += trans[i][0]

    return ret
