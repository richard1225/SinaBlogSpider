# -*- coding: utf-8 -*-  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from blog.items import BlogItem
from scrapy.conf import settings
import requests

class MyblogSpider(CrawlSpider):  

    #spider name
    name = 'updateblog'
    allowed_domain = ['blog.sina.com.cn']  

    #crawl from following urls
    start_urls = [  'http://blog.sina.com.cn/s/articlelist_1434387020_0_1.html'						
                    'http://blog.sina.com.cn/s/articlelist_1279884602_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1409928055_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1216826604_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_3138175493_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_3820883734_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1349323031_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1319802272_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1503491352_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1233227211_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1649821184_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1504965870_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1298535315_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1284139322_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1236135807_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1300871220_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_2323935385_0_7.html',						
                    'http://blog.sina.com.cn/s/articlelist_1364334665_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_3996792112_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1282871591_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1650676404_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1751100587_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1791653972_0_1.html',						
						
                    'http://blog.sina.com.cn/s/articlelist_1305431810_0_1.html', 						
                    'http://blog.sina.com.cn/s/articlelist_1279916282_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1243881594_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1638714710_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1182426800_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1243037810_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1278226564_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_3602486214_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1285707277_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1617732512_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1190841165_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1713769794_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_2709103937_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1252364410_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1736521680_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1789788500_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1168504694_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_2243873437_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1192082717_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_2373950562_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1269486882_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1747635343_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1278127565_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1725765581_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1661526105_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1307309734_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1349341797_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_3261332971_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1730637475_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_5036518671_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1378170044_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_3021571764_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1699909555_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_3973200582_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1117176112_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1197803434_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1259215934_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1905024361_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_5889347520_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1303588263_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1223891223_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_2294788952_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1095876111_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1227422602_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1377494453_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1566313620_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1689531444_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1147012071_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1558171353_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1195167233_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1581557932_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1278215885_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1301047350_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1319475951_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1092849864_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1239417764_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1290677635_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1273642560_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1317254782_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1503072772_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1220069571_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_2377371197_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1253039302_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1225255825_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1502620537_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1724710054_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1507817532_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1394379401_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1338707944_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1253205351_0_1.html',						
                    'http://blog.sina.com.cn/s/articlelist_1301484230_0_1.html' ]

    #设置深挖规则
    rules = [  
        # Rule(LinkExtractor(allow=r'/s/articlelist_\d+')),  
        Rule(LinkExtractor(allow=r'/s/blog_\d+'), callback="parse_item"),  
    ]  
  
    def parse_item(self, response):  
        items = BlogItem()
        sel = Selector(response)
        btitle = sel.xpath('//*[@class="articalTitle"]/h2/text()').extract()[0].encode('utf-8')
#        item['title'] = sel.xpath('//*[@class="link_title"]/a/text()').extract()[0].encode('utf-8')  
        btime = sel.xpath('//*[@class="time SG_txtc"]/text()').extract()[0]
        bcontents = sel.xpath('//font[contains(@size, "+0")]/text()').extract()
        boldcontents = sel.xpath('//b/text()').extract()
        boldfont = sel.xpath('//b/font/text()').extract()
        
        like = "".join(response.xpath('//*[@class="IL"]//text()').extract())

        print('yuedu/r/n'+like)

        #获取文章的主要内容
        acontent = "".join(response.xpath('//div[@id="sina_keyword_ad_area2"]//text()').extract())
        bcontent = ''
        for content in bcontents:
            bcontent += content.encode('utf-8')
        for bold in boldcontents:
            bcontent += bold.encode('utf-8')
        if boldfont != []:
            bcontent += boldfont[0].encode('utf-8')
        
        #获取时间
        btime=btime.replace('(','')
        btime=btime.replace(')','')

        # 初步去除内容的回车
        acontent = acontent.replace('\n','')
        acontent = acontent.replace('\t','')

        # 获取名字id
        nameid = response.css('link[rel*=alternate]::attr(href)').extract()[0].split('/')[-1].split('.')[0]
        name = requests.get('http://uic.sso.sina.com.cn/uic/Mutiquery.php?UID=0&Check=null&UIDS=[' + nameid + ']&UserInfoTypes=[1]&ProductType=2&varname =requestId_8481872').content.split('"')[-2].decode("unicode-escape")

        # 获取阅读量
        viewids = response.url.split('_')[-1].split('.')[0].split('01')
        con = requests.get('http://comet.blog.sina.com.cn/api?maintype=num&uid=' + viewids[0] + "&aids=" + viewids[1] + "&requestId=aritlces_number_3610").content
        arr = con.split('{')[-1].split('}')[0].split(',')
        view = 0
        like = 0
        comment = 0
        for a in arr:
            if a.find("r") != -1:
                print ("\r\n\r\n\r\n"+a.split(":")[-1]+"\r\n\r\n\r\n")
                view = a.split(":")[-1]
            if a.find("d") != -1:
                like = a.split(":")[-1]


        # 存入数据库
        items['name'] = name 
        items['time'] = btime
        items['title'] = btitle
        items['content'] = acontent
        items['view'] = view
        items['like'] = like
        items['arturl'] = response.url
        yield items
        # print(items)
        # print(btitle + "\r\n  时间："+btime+"\r\n博文片段: ")
        # # print(bcontent + "\r\n\r\n")
        # print(acontent+"\r\n")

