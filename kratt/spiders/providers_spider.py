# -*- coding: utf-8 -*-

import scrapy
from kratt.items import ProviderItem

def attempt_extract_css(parent, query):
    node = parent.css(query)
    if node is not None:
        return node.extract_first()
    else:
        return None
            
class ProviderSpider(scrapy.Spider):
    name = "providers"
    
    def start_requests(self):
        url = 'https://www.1182.ee/'
        search_word = getattr(self, 'search_word', None)
        field = None
        if search_word is not None:
            url += 'otsing/' + search_word
        else:
            field = getattr(self, 'field', None)
            if field is not None:
                url += field
        
        if search_word is not None or field is not None:
            location = getattr(self, 'location', None)
            if location is not None:
                url += '/' + location
            yield scrapy.Request(url, self.parse)
    
    def parse_details(self, response):
        provider_item = response.meta['provider_item']
        provider_item['e_mail'] = attempt_extract_css(response, 'div.company-single a.mail-form::text')
        registry_num = attempt_extract_css(response, 'div.company-single h4.icon_company_reg_code a::text')
        if registry_num is not None:
            provider_item['registry_num'] = registry_num[:registry_num.find(' ')]
        else:
            provider_item['registry_num'] = None
        yield provider_item
  
    def parse(self, response):
        for provider in response.css('.company-view-all'):
            provider_item = ProviderItem()
            details_url = response.urljoin(provider.css('a.company-profile-link::attr(href)').extract_first())
            provider_item['name'] = attempt_extract_css(provider, 'a.company-profile-link::text')
            request = scrapy.Request(details_url, callback=self.parse_details)
            request.meta['provider_item'] = provider_item
            yield request
            
        next_page = response.css('a.pn-next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)