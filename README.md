# Python实现文档自动翻译 #
## 目的 ##
本文旨在说明Python文档自动翻译的需求分析以及实现过程。 

## 需求分析 ##
因在工作中，经常需要浏览英文文档，然而对于英文不太好的我来说，有时需要借助谷歌或者百度翻译，但文档往往比较长，复制粘贴很麻烦，所以心里就萌生了一个想法，看能不能自动对文档进行翻译，并生成文档，想法是可以的，实现应该是可行的，所以决定撸起袖子就是干！  
### 选择Python ###
为什么选择Python：  
1）因为人生苦短；  
2）因为刚好在学习AI；  

好了，废话就这么多，进入主题。  
### 功能需求 ###

· 用户可选择谷歌、百度和有道翻译，后期可考虑添加其他的接口；  
· 实现PDF、Word、TXT等多种类型的文档翻译，程序自动识别文档类型；  
· 翻译后生成的新文档格式可以为PDF、Word、TXT格式（未实现）;  
· 有日志记录文件。

## 关键方法 ##

### 提取文档内容 ###
#### 读取TXT文档 ####
txt文档的读取很简单，直接用python自带的open()方法就好，代码如下所示：  

	# 读取TXT文档
	def read_txt(path):
	    '''实现TXT文档的读取，一次将内容全部取出'''
	    content = ''
	    with open(path) as f:
	        content = f.read()
	    return content
	# 也可以用readline()读取每一行

#### 读取Word文档 ####
读取Word文档也比较简单，导入第三方库python-docx，安装指令为pip install python-docx，实例代码如下：  


	import docx    # 安装指令：pip install python-docx

    def translate(self):
        '''翻译'''

        # 获取文档对象
        doc = docx.Document(self.fullName)

        # 创建内存中的word文档对象
        new_doc = docx.Document()

        # 遍历每一段文本
        for para in doc.paragraphs:
            # 翻译
            trans = baidu_translate(para.text)           
            # 写入新文件
            new_doc.add_paragraph(para.text)
            new_doc.add_paragraph(trans)

        # 保存到本地文件
        new_doc.save(self.new_fullPath)
       
#### 读取PDF文档 ####
读取PDF文档同样需要安装第三方库，主要有PyPDF2和pdfminer，这两个库我都有去了解，算是各有特点吧。  
PyPDF2使用相对简单，但只支持英文，对中文支持不太友好；相反pdfminer使用相对而言要复杂点，仅仅是相对而言，其支持多种语言，图表、图片等，功能较强大。这两种方式我在代码中均有实现，其实例代码如下：  
**PyPDF2**

	# 安装指令：pip install pypdf2
	from PyPDF2.pdf import PdfFileReader

    def translate(self):
        '''读取pdf内容，并翻译，写入txt文件'''
        f = open(self.fullPath,'rb')
        pdf = PdfFileReader(f)

        for i in range(0,pdf.getNumPages()):
            extractedText = pdf.getPage(i).extractText()
            content = extractedText.split('\n')  
            content = self.removeBlankFromList(content)  

            # 拼接之后的文本，如果单词间歇超过一个空格的，认为是需要换行处理的
            content_list = self.enter_symbol(content)

            for line in content_list:
                trans = baidu_translate(line)
                self.write(line + '\n')
                self.write(trans)

        f.close()
        Logger().write(self.fileName + '翻译完成，新文档：' + self.new_fullPath)

**pdfminer**

	# 安装指令：pip install pdfminer3k
	from pdfminer.pdfparser import PDFParser,PDFDocument
	from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
	from pdfminer.layout import LAParams,LTTextBoxHorizontal
	from pdfminer.converter import PDFPageAggregator
	from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

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
                        content = out.get_text()
                        trans = baidu_translate(content)
                        self.write(content)
                        self.write(trans)
            Logger().write(self.fileName + '翻译完成，新文档：' + self.new_fullPath)


### 调用翻译接口 ###
利用python网络爬虫可以很轻松的实现数据爬取，这里就是利用这种“手段”实现翻译功能，对此，还是要感谢这些接口提供商，感谢CCTV、铁岭TV。
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
	    with open(path,'a+') as f:
	        f.write(content)

#### 写Word文档 ####
Word文档的写就是用上面所属的python-docx库实现，在上面读取Word文档小节中已有代码明细，非常之简单，这里就不在赘述。
#### 写PDF文档 ####
同上，写PDF文档，用PyPdf和pdfminer均可实现，PyPDF相对而言要简单写，因本脚本对翻译后的文档只实现了Word和TXT的写，方便对文档进行编辑处理，若需要生成PDF文档，有兴趣可自行研究。

好了，关键技术已基本描述清楚，下面就是具体的实现过程和效果对比。

## 实现 ##
实现过程就是怼代码的过程，思路有了，自然信手拈来，语法不清楚的可以google、百度，我也是个python新手，代码只是思路的体现，没多少含金量，只是熟能生巧罢了。所以这里就不贴代码，如需查看我丑陋的代码，等下我会把代码共享到全球最大的同性交友网站，您可自取。
### 效果 ###
我准备了著名的演讲马丁·路德·金的《我有一个梦想》英文版3种不同格式的文档，如下图所示：
![](https://i.imgur.com/XyX2UMy.png)  
运行Python脚本，如下图所示：  
![](https://i.imgur.com/4W721ir.png)  
查看生成的文档，如下图所示：  
![](https://i.imgur.com/okLXGmM.png)  
翻译前后对比**（TXT）**
![](https://i.imgur.com/5PZw7ko.png)  
翻译前后对比**（Word）**
![](https://i.imgur.com/O09nMEB.png)
翻译前后对比**（PDF）**
![](https://i.imgur.com/6IWdcBq.png)

嗯！大概就是这样的。

## 分享 ##
本项目的地址：[https://github.com/wangxijin/TranslateTool](https://github.com/wangxijin/TranslateTool)  
如有问题，可以与我交流。  

Allen   
June 23,2018  
Chengdu