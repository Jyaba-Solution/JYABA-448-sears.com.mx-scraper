import scrapy
import datetime
import json
import re

'''
Date == Script run date  (DD/MM/YYYY) 
Canal == “Sanborns” 
Category == category 
Subcategory = Subcategory 
Subcategory2= Subcategory2 
Subcategory3=  BLANK 
Marca == Brand 
Modelo == Model 
SKU ==SKU 
UPC == UPC 
Item == Item 
Item Characteristics == Item Characteristics 
URL SKU == URL 
Image == image 
Price == Price 
Sale Price == Sale Price 
Shipment Cost == BLANK 
Sales Flag == Sales Flag 
Store ID == BLANK 
Store Name = BLANK 
Store Address = BLANK 
Stock == Stock 
UPC WM == UPC[0:-1].zifll(16) 
Final Price == min (price, sale price). 
'''

# https://www.sears.com.mx/
class SearsSpider(scrapy.spiders.SitemapSpider):
    name = 'sears'
    sitemap_urls = ['https://www.sears.com.mx/sitemap.xml']
    sitemap_rules = [('/products/','parse_category')]

    def parse_category(self, response):
        urls = re.findall(r'/producto/(.+?)/', response.text)
        new_urls = [f'https://seapi.sears.com.mx/app/v1/product/{product_id}' for product_id in urls]
        for url in new_urls:
            yield scrapy.Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        product_json = response.json()
        item = {}
        item['Date'] = datetime.datetime.now().strftime('%d/%m/%Y')
        item['Canal'] = 'Sanborns'
        categories_list = product_json.get('data',{}).get('categories')
        categories_dict = {x:y.get('name') for x,y in enumerate(categories_list)}
        item['Category'] = categories_dict.get(0)
        item['Subcategory'] = categories_dict.get(1)
        item['Subcategory2'] = categories_dict.get(2)
        item['Subcategory3'] = ''
        item['Marca'] = product_json.get('data',{}).get('brand')
        item['Modelo'] = product_json.get('data',{}).get('model')
        item['SKU'] = product_json.get('data',{}).get('sku')
        item['UPC'] = product_json.get('data',{}).get('ean')
        item['Item'] = product_json.get('data',{}).get('title')
        item['Item Characteristics'] = product_json.get('data',{}).get('description')
        yield item

        breakpoint()
        
   