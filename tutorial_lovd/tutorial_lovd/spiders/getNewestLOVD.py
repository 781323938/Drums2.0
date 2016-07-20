#encoding:utf8
import scrapy
import datetime
#from scrapy.spiders import Spider
import json
LOVDDict = {}
class MySpider(scrapy.Spider):
    name = 'get_newest_lovd_url'
    allowed_domains = ['grenada.lumc.nl']
    start_urls = ["http://grenada.lumc.nl/LSDB_list/ajax/viewlist.php?viewlistid=LSDBs&object=LSDB&id=0&order=symbol%2CASC&page_size=1000&page={page}".format(page=str(page)) for page in range(1,94)]
    def parse(self,response):
        global LOVDDict
        rows = response.xpath('//tr[@class="data"]')
        itemDict = {}
        for j in range(len(rows)):
            cols = rows[j].xpath('.//td')
            geneName = cols[0].xpath('.//text()').extract()[0]
            databaseURL = cols[1].xpath('.//a/text()').extract()[0]
            #withDisease = cols[6].xpath('.//text()').extract()[0]
            updateDate = cols[6].xpath('.//text()').extract()[0]
            if geneName not in LOVDDict:
                LOVDDict[geneName] = {}
                LOVDDict[geneName]['updateDate'] = ''
                LOVDDict[geneName]['databaseURL'] = ''
            if updateDate == 'Unknown' and LOVDDict[geneName]['updateDate'] == '':
                LOVDDict[geneName]['updateDate'] = '1900-01-01'
                LOVDDict[geneName]['databaseURL'] = databaseURL
            elif updateDate != 'Unknown':
                if LOVDDict[geneName]['updateDate'] == '':
                    LOVDDict[geneName]['updateDate'] = updateDate
                    LOVDDict[geneName]['databaseURL'] = databaseURL
                else:
                    newDateForm = int(updateDate.replace("-",""))
                    oldDateForm = int(LOVDDict[geneName]['updateDate'].replace("-",""))
                    if newDateForm > oldDateForm:
                        LOVDDict[geneName]['updateDate'] = updateDate
                        LOVDDict[geneName]['databaseURL'] = databaseURL
            print databaseURL
        LOVDDictFile = 'knols/LOVDDict.json'
        content = json.dumps(LOVDDict,indent=2)
        f = open(LOVDDictFile,'w')
        f.write(content)
        f.close()
        print itemDict
