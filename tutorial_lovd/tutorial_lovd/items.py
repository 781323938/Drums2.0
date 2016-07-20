# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LovdItem(scrapy.Item):
    # define the fields for your item here like:
    Gene_symbol = scrapy.Field()
    Gene_name = scrapy.Field()
    Chromosome = scrapy.Field()
    Chromosomal_band = scrapy.Field()
    Genomic_reference = scrapy.Field()
    Associated_diseases = scrapy.Field()
