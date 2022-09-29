import scrapy
import datetime
import json
import re



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

        try:
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
            item['Item Characteristics'] = product_json.get('data',{}).get('description').replace('\n',' ') + ' ' + str(product_json.get('data',{}).get('attributes'))
            item['URL SKU'] = f'https://www.sears.com.mx/producto/{product_json.get("data").get("id")}/{product_json.get("data",{}).get("title_seo")}'
            item['Image'] =  product_json.get('data',{}).get('images')[0]['url']
            item['Price'] = product_json.get('data',{}).get('price')
            item['Sale Price'] = product_json.get('data',{}).get('sale_price')
            item['Shipment Cost'] = ''
            item['Sales Flag'] = str(product_json.get('data',{}).get('discount')) + '%' if product_json.get('data',{}).get('discount') else ''
            item['Store ID'] = ''
            item['Store Name'] = ''
            item['Store Address'] = ''
            item['Stock'] = product_json.get('data',{}).get('stock')
            item['UPC WM'] = str(product_json.get('data',{}).get('ean'))[0:-1].zfill(16)
            item['Final Price'] = min(product_json.get('data',{}).get('price'), product_json.get('data',{}).get('sale_price'))
            item['Store ID'] = ''
            item['Store Name'] = ''
            item['Store Address'] = ''
            item['Stock'] = product_json.get('data',{}).get('stock')
            item['UPC WM'] = str(product_json.get('data',{}).get('ean'))[0:-1].zfill(16)
            item['Final Price'] = min(product_json.get('data',{}).get('price'), product_json.get('data',{}).get('sale_price')) if product_json.get('data',{}).get('sale_price') else product_json.get('data',{}).get('price')   
            yield item
        except Exception as e:
            print(e)
            

        
   