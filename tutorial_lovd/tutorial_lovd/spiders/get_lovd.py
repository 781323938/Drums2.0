#encoding:utf8
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from tutorial_lovd.items import LovdItem

class MySpider(CrawlSpider):
    name = 'get_lovd'
    allowed_domains = ['databases.lovd.nl']
    start_urls = ['http://databases.lovd.nl/shared/genes#id=0&order=id_%2CASC&skip[geneid]=geneid&search_diseases_=-&page_size=1&page=1']
    rules = (Rule(LinkExtractor(allow=('http://databases.lovd.nl/shared/genes/.+',)),callback='parse_item'),)
    def parse_item(self,response):
        item = LovdItem()
        tables = response.xpath('//table/tr/td/table[@class="data"]')
        print len(tables)
        itemDict = {}
        for j in range(len(tables)):
            titles = tables[j].xpath('.//tr/th/text()').extract()
            #print titles
            values = tables[j].xpath('.//tr/td')
            if titles and values:
                print len(titles),len(values)
                #raw_input()
                for i in range(1,len(titles)):
                    finalTitle = titles[i].replace(u'\xa0','_').encode('utf8').strip()
                    value = values[i-1].xpath('.//text()').extract()[0].encode('utf8').strip()
                    if finalTitle == 'Associated_with_diseases' and value == '-':
                        return None
                for i in range(1,len(titles)):
                    valueList = []
                    if values[i-1].xpath('.//a/text()'):
                        value = values[i-1].xpath('.//a/text()').extract()
                        url = values[i-1].xpath('.//a/@href').extract()
                        for l in range(len(value)):
                            finalValue = value[l].encode('utf8').strip()
                            finalUrl = url[l].encode('utf8').strip()
                            if 'http' not in finalUrl:
                                finalUrl = urljoin_rfc(get_base_url(response),finalUrl)
                            valueList.append((finalValue,finalUrl))
                    else:
                        value = values[i-1].xpath('.//text()').extract()
                        for l in range(len(value)):
                            finalValue = value[l].encode('utf8').strip()
                            valueList.append((finalValue,''))
                    finalTitle = titles[i].replace(u'\xa0','_').encode('utf8').strip()
                    #print finalTitle,":", valueList
                    itemDict[finalTitle] = valueList
        print itemDict