# -*- coding: utf-8 -*-
import scrapy
from drums2.DrumsNLP import utils as drumsUtils
from drums2.items import MiniVarInfo

class Abca12Spider(scrapy.Spider):
    name = "ABCA12"
    allowed_domains = ["www.med.nagoya-u.ac.jp"]
    start_urls = (
        'https://www.med.nagoya-u.ac.jp/derma/ABCA12/',
    )

    def parse(self, response):
        sContent = ''.join(response.xpath('//text()').extract())
        
        heads = []
        for mutation in response.xpath('//table[@bgcolor="#000000"]/tr'):
            for head in mutation.xpath('.//td/span/text()').extract():
                heads.append(head)
            break
        skip_first = True
        for mutation in response.xpath('//table[@bgcolor="#000000"]/tr'):
            if skip_first:
                skip_first = False
                continue
                
            for item in mutation.xpath('.//td'):
                variant = MiniVarInfo()
                print item.xpath('.//text()').extract_first()
                print item
                paper_url = item.xpath('.//a/@href').extract_first()
                if paper_url:
                    variant['reference_info'] = {'pmid': drumsUtils.getPubmedIDFromURL(paper_url)}
                else:
                    variant['reference_info'] = {}
   
            yield variant
