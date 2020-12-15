# -*- coding: utf-8 -*-
from config import domain, sum_key
from utils.get_data import get_soup
import json
from utils.mysql_class import MySQL


class ProductList:
    def __init__(self, page_link, id_category):
        data = get_soup(url=page_link)
        self.soup = data[1]
        self.text = data[0]
        self.products = None
        self.id_category = id_category

    @property
    def this_is_product_list(self):
        try:
            if len(self.soup.find_all('div', attrs={'id': 'goodsBlock'})) or ('window.__APP__=' in self.text):
                return True
        except:
            pass
        return False

    @property
    def this_is_404_page(self):
        try:
            if self.soup.find_all('div', attrs={'class': 'page-404'}):
                return True
        except:
            pass
        return False

    @property
    def contains_product(self):
        try:
            if 'window.__APP__=' in self.text:
                scripts = self.soup.find_all('script')
                js_products = scripts[0].string.split('window.__APP__=')[-1].strip().replace('undefined', 'null')
                js = json.loads(js_products)
                dict_products = dict(js)
                products = []
                for item in dict_products['cmp'][0]['listingData']['items']:
                    products.append({
                        'id': item['goods']['goodsId'],
                        'name': item['goods']['title'],
                        'category': '',
                        'price': item['price'],
                        'brand': item['goods']['brand'],
                        'price_last': item['lastPrice']

                    })
            else:
                text = self.text.split('_GOODS_.catalog_page = ')[-1].split('_GOODS_.gaPushInitData = ')[0].strip().strip(';')
                js = json.loads(text)
                products = dict(js)['items']

            if len(products) > 0:
                self.products = products
                return True
        except:
            pass
        return False

    def get_and_write_products(self):
        for index, product in enumerate(self.products, start=0):
            try:
                link_product = domain + self.soup.find('a', attrs={'data-product-sku': product['id']})['href']
                self.products[index]['link'] = link_product
                MySQL().write_product(product=product, link_product=link_product, id_category=self.id_category)
            except:
                pass
        return self.products


if __name__ == '__main__':
    ps = ProductList(page_link='https://goods.ru/catalog/chajniki-elektricheskie/', id_category=2)
    a = ps.this_is_product_list
    b = ps.contains_product
    c = ps.this_is_404_page
    print(a, b, c)
    if a and b and not c:
        products_ = ps.get_and_write_products()
        for i in products_:
            print(i)

