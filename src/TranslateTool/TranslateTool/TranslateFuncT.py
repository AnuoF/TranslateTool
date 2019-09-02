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
import requests   # pip intasll requests
from Py4Js import *
from Logger import *


# 百度翻译方法
def baidu_translate(content,type=1):
    '''实现百度翻译'''
    # 需要 sign 和 Cookie，而且query/sign/Cookie三者之间有关联关系。 此问题暂未解决  2019/3/4 

    baidu_url = "https://fanyi.baidu.com/v2transapi"
    data = {}
    data['from'] = 'zh'
    data['to'] = 'en'
    data['query'] = "妈妈"    # 奶奶
    data['transtype'] = 'translang'     # enter/realtime/translang : 经测试，此处填什么内容无影响
    data['simple_means_flag'] = '3'
    data['sign'] = '64344.268393'  # 422672.167969
    data['token'] = 'b08c1ff5373f47e4a5b62c59d38d4f63'
    data = urllib.parse.urlencode(data).encode('utf-8')

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
    #headers['Referer'] = 'https://fanyi.baidu.com/translate?aldtype=16047&query=&keyfrom=baidu&smartresult=dict&lang=auto2zh'   # 可以不需要
    headers['Cookie'] ='BAIDUID=09546BF566035455B10181ED1091C5B1:FG=1; BIDUPSID=09546BF566035455B10181ED1091C5B1; PSTM=1551086333; BDUSS=1mMmtwVjc1RnBtR05mMUljOC13amFabjBZRn5HY2JKRUJnWkV1bTBMVWdoWjFjQVFBQUFBJCQAAAAAAAAAAAEAAAAACYVHUmF5X0EzNGVuAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACD4dVwg-HVcYW; MCITY=-75%3A; pgv_pvi=4361364480; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=3; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; pgv_si=s991542272; locale=zh; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; H_PS_PSSID=26525_1440_25809_21122_20697_28585_26350_28603_28415; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1551663602,1551670352; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1551670352; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D'

    baidu_re = urllib.request.Request(baidu_url, data, headers=headers)
    baidu_response = urllib.request.urlopen(baidu_re)
    baidu_html = baidu_response.read().decode('utf-8')
    target2 = json.loads(baidu_html)

    trans = target2['trans_result']['data'][0]['dst']
    ret = ''
    for i in range(len(trans)):
        ret += trans[i]['dst'] + '\n'

    if ret:
        return (True,ret)
    else:
        return (False,ret)


    #baidu_url = 'http://fanyi.baidu.com/basetrans'
    #data = {}

    #data['from'] = 'en'
    #data['to'] = 'zh'
    #data['query'] = content
    #data['transtype'] = 'translang'
    #data['simple_means_flag'] = '3'
    #data['sign'] = '94582.365127'
    #data['token'] = 'ec980ef090b173ebdff2eea5ffd9a778'
    #data = urllib.parse.urlencode(data).encode('utf-8')

    #headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}
    #baidu_re = urllib.request.Request(baidu_url, data, headers)
    #baidu_response = urllib.request.urlopen(baidu_re)
    #baidu_html = baidu_response.read().decode('utf-8')
    #target2 = json.loads(baidu_html)

    #trans = target2['trans']
    #ret = ''
    #for i in range(len(trans)):
    #    ret += trans[i]['dst'] + '\n'

    #if ret:
    #    return (True,ret)
    #else:
    #    return (False,ret)


# 有道翻译方法
def youdao_translate(content):
    '''实现有道翻译的接口'''

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=https://www.baidu.com/link'
    #url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = {
        'from':'Auto',
        'to':'Auto',
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
    ret = ta['translateResult'][0][0]['tgt']

    if ret:
        return (True,ret)
    else:
        return (False,ret)

    # 下面的代码不能使用!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    youdao_url = 'http://fanyi.youdao.com/translate'  
    data = {}
    
    data['i']= content
    data['from'] = 'Auto'
    data['to'] = 'Auto'
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
  
    #result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=zh-CN 
        # &tl=en&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss 
        # &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)  

    result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=zh-CN&tl=en&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss 
        &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)
  
    #返回的结果为Json，解析为一个嵌套列表  
    trans = result.json()[0]
    ret = ''
    for i in range(len(trans)):
        line = trans[i][0]
        if line != None:
            ret += trans[i][0]

    if ret:
        return (True,ret)
    else:
        return (False,ret)


def translate_func(content):
    '''集成百度、谷歌、有道多合一的翻译'''

    funcs = [google_translate, youdao_translate]    # baidu_translate,google_translate,youdao_translate
    count = 0

    # 循环调用百度、谷歌、有道API，其中如果谁调成功就返回，或者大于等于9次没有成功也返回。
    while True:
        for i in range(len(funcs)):
            ret = (False,'')
            try:
                ret = funcs[i](content)
            except:
                Logger().write("调用 %s 方法出现异常。" % funcs[i].__name__)

            if ret[0] == True:
                return ret[1]
            else:
                count += 1
                if count >= 9:
                    Logger().write("以下内容尝试9次仍翻译失败，内容【 %s 】" % content)
                    return ''
                else:
                    continue
