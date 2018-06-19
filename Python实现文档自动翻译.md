# Python实现文档自动翻译 #

## 目的 ##
本文旨在说明Python文档自动翻译的需求分析以及实现过程。 

## 需求分析 ##
因在公司开发过程中，经常需要浏览英文文档，然而对于英文不太好的我来说，需要借助谷歌或者百度翻译，但文档往往比较长，复制粘贴很麻烦，所以心里就萌生了一个想法，看能不能自动对文档进行翻译，并生成文档，想法是可以的，实现应该是可行的，所以决定撸起袖子就是干！  
### 选择Python ###
为什么选择Python：  
1）因为人生苦短；  
2）加上最近刚好在学些Python。 

好了，废话就这么多，进入主题。  
### 功能需求 ###
既然要做，就希望把它做得漂亮一点，此工具的功能需求如下：  
1）做成UI界面的程序，便于用户操作（在后期考虑）；  
2）用户可选择谷歌或者百度翻译，后期可考虑添加其他的接口；  
2）实现PDF、Word、TXT等多种类型的文档翻译，程序自动识别文档类型；  
3）翻译后生成的新文档格式可以为PDF、Word、TXT格式，可以由用户选择；  
4）有日志记录文件，日志记录的方式为覆盖记录，即程序开始时会自动删除之前存在的文件，在执行过程中记录日志。

## 关键过程 ##

### 原型界面 ###
![](https://i.imgur.com/3PLRJeW.png)
### 读取文档内容 ###
#### 读取TXT文档 ####
txt文档的读取很简单，直接用python自带的open()方法就好，代码如下所示：  

	# 读取TXT文档
	def read_txt(path):
	    '''实现TXT文档的读取，一次将内容全部取出'''
	    content = ''
	    with open(path) as f:
	        content = f.read()
	    return content

#### 读取Word文档 ####
#### 读取PDF文档 ####
### 调用翻译接口 ###
#### 百度翻译 ####

百度翻译有反爬机制，电脑端的爬虫会被干掉，所幸手机端可以使用，代码如下所示：  
	
	import urllib.request  
	import urllib.parse  
	import json 

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


#### 谷歌翻译 ####

参考 [https://blog.csdn.net/yingshukun/article/details/53470424](https://blog.csdn.net/yingshukun/article/details/53470424)

首先需要一个类实现JS码的生成

	
	import execjs  
	  
	class Py4Js():  
	      
	    def __init__(self):  
	        self.ctx = execjs.compile(""" 
	        function TL(a) { 
	        var k = ""; 
	        var b = 406644; 
	        var b1 = 3293161072; 
	         
	        var jd = "."; 
	        var $b = "+-a^+6"; 
	        var Zb = "+-3^+b+-f"; 
	     
	        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
	            var m = a.charCodeAt(g); 
	            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
	            e[f++] = m >> 18 | 240, 
	            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
	            e[f++] = m >> 6 & 63 | 128), 
	            e[f++] = m & 63 | 128) 
	        } 
	        a = b; 
	        for (f = 0; f < e.length; f++) a += e[f], 
	        a = RL(a, $b); 
	        a = RL(a, Zb); 
	        a ^= b1 || 0; 
	        0 > a && (a = (a & 2147483647) + 2147483648); 
	        a %= 1E6; 
	        return a.toString() + jd + (a ^ b) 
	    }; 
	     
	    function RL(a, b) { 
	        var t = "a"; 
	        var Yb = "+"; 
	        for (var c = 0; c < b.length - 2; c += 3) { 
	            var d = b.charAt(c + 2), 
	            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
	            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
	            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
	        } 
	        return a 
	    } 
	    """)  
	          
	    def getTk(self,text):  
	        return self.ctx.call("TL",text)  

调用方法如下所示：

	from Py4Js import *

	# 谷歌翻译方法
	def google_translate(content):
	    '''实现谷歌的翻译'''
	    js = Py4Js()
	    tk = js.getTk(content)
	
	    if len(content) > 4891:      
	        print("翻译的长度超过限制！！！")      
	        return    
	  
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

#### 有道翻译 ####
有道翻译的代码实现如下所示：

	import urllib.request  
	import urllib.parse  
	import json 

	# 有道翻译方法
    def youdao_translate(content):
	    '''实现有道翻译的接口'''
	    youdao_url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
	    data = {}
	    
	    data['i']= content
	    data['from'] = 'AUTO'
	    data['to'] = 'AUTO'
	    data['smartresult'] = 'dict'
	    data['client'] = 'fanyideskweb'
	    data['salt'] = '1525141473246'
	    data['sign'] = '47ee728a4465ef98ac06510bf67f3023'
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

### 写入文档 ###
#### 写TXT文档 ####
TXT文档的写比较简单，代码如下所示：

	# 写TXT文档
	def write_txt(path,content):
	    '''实现TXT文档的写方法'''
	    with open(path,'w') as f:
	        f.write(content)

#### 写Word文档 ####
