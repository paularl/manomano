import scrapy
import re
import datetime
from scrapy.linkextractors import LinkExtractor

class ManoManoSpyder(scrapy.Spider):

    name = 'manomano_diferenciales'
    allowed_domains = ['manomano.fr']
    start_urls = ['https://www.manomano.fr/interrupteur-et-disjoncteur-differentiel-2013',
                  'https://www.manomano.fr/disjoncteur-modulaire-220',
                  'https://www.manomano.fr/tableau-electrique-pre-equipe-2011']


    def parse(self, response):

        print("procesing:"+response.url+'..............................................................................')
        # #Extract data using css selectors
        product_title = response.xpath('*//div[@class="product-card-root products__product card-root"]/a/@title').extract()
        product_price = response.xpath('*//div[@class="product-card-root products__product card-root"]/a/@data-product-price').extract()
        product_b2b = response.xpath('*//div[@class="product-card-root products__product card-root"]/a/@data-is-b2b').extract()
        product_business_score = response.xpath('*//div[@class="product-card-root products__product card-root"]/a/@data-business-score').extract()
        product_transport = response.xpath('*//div[@class="characteristic__label"]/text()').extract()
        product_brand = response.xpath('*//div[@class="image-block product-card-root__image-block"]').extract()
        product_url = response.xpath('*//div[@class="product-card-root products__product card-root"]/a/@href').extract()
        print("uoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        print(response.request.url)
        cat = response.request.url.split('/')[-1]

        row_data = zip(product_title, product_price, product_b2b, product_business_score, product_transport,
                       product_brand, product_url)
        #Making extracted data row wise
        for item in row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
                #key:value
                'titulo': item[0].replace(",",'.'),
                'precio': float(item[1]),
                'esb2b': item[2],
                'business_score': float(item[3]),
                'transporte': re.findall("\d+\.\d+",item[4]),
                'marca': self.extract_brand(item[5]),
                'url': 'https://www.manomano.fr/catalogue'+item[-1],
                'categoria': self.extract_category(cat),
                'date': datetime.datetime.today().date()
            }

            #yield or give the scraped info to scrapy
            yield scraped_info

        next_page = response.css('li.pagination__item.pagination__item--next a::attr(href)').get()
        if next_page is not None:
              print("---------------------- changing page")
              yield response.follow(next_page, encoding='latin-1', callback=self.parse)

    @staticmethod
    def extract_brand(brand_item):
        from lxml import etree

        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(brand_item, parser)

        if 'brand--logo-image' in brand_item:
            vals_image = root.find('./div/img').values()
            brand = vals_image[-1].split('-')[1]
        elif "brand__brand-text" in brand_item:
            brand = root.find('./div/p').text
        else:
            brand = None

        return brand

    @staticmethod
    def extract_category(cat_item):

        if 'interrupteur-et-disjoncteur-differentiel' in cat_item:
            return "diferenciales"
        elif 'disjoncteur-modulaire' in cat_item:
            return 'disjuntores_modulares'
        elif 'tableau-electrique' in cat_item:
            return "cuadros"

