# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProviderItem(scrapy.Item):
	name = scrapy.Field()
	registry_num = scrapy.Field()
	e_mail = scrapy.Field()
