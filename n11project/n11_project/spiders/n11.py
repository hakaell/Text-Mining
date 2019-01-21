# -*- coding: utf-8 -*-
import json
import csv
import scrapy

class N11Spider(scrapy.Spider):
    name = 'n11'
    start_urls = ['https://www.n11.com/']
    download_delay = 0.001

    def parse(self,response):
        categories_url = response.css('li.subCatMenuItem a::attr(href)').extract()
        categories_url.remove('https://www.n11.com/moda11')
        categories_url.remove('https://www.n11.com/market11')
        categories_url.remove('https://www.n11.com/promosyon/luks-kozmetik-482262')
        categories_url.remove('https://www.n11.com/lastik-ve-jant/oto-lastik')
        for url in categories_url:
            yield scrapy.Request(url=url, callback=self.parse_productList)

    def parse_productList(self, response):
        product_links = response.css('section.group li.column a.plink::attr(href)').extract()
        for pro_link in product_links:
            yield response.follow(pro_link, callback=self.parse_product)
        if response.css('div.pagination a.next::attr(href)').extract_first():
            next_page_link = response.css('div.pagination a.next::attr(href)').extract_first()
            yield scrapy.Request(url=next_page_link, callback= self.parse_productList)

    def parse_product(self, response):
        pro_title = response.css('h1.proName::text').extract_first().replace('\n', ' ').strip()
        pro_categories = response.css('div.breadcrumb a::attr(title)').extract()
        yield_value = [pro_title] + pro_categories
        urunDict = {}
        urunDict["Description"] = yield_value[0]
        for i in range(1, len(yield_value)):
            urunDict[str(i) + ". Category"] = yield_value[i]
        yield urunDict