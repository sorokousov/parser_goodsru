# -*- coding: utf-8 -*-
from config import domain, sum_key
from utils.get_data import get_soup
import json
from utils.mysql_class import MySQL


class ProductMain:
    def __init__(self, page_link, sku):
        data = get_soup(url=page_link)
        self.soup = data[1]
        self.text = data[0]
        self.products = None
        self.sku = sku

    def this_is_product_main(self):


    def images(self):
        try:
            if len(self.soup.find_all('div', attrs={'id': 'goodsBlock'})) or ('window.__APP__=' in self.text):
                return True
        except:
            pass
        return False

    def descriptions(self):
        try:
            if self.soup.find_all('div', attrs={'class': 'page-404'}):
                return True
        except:
            pass
        return False

    def write_product(self):
        for index, product in enumerate(self.products, start=0):
            try:
                link_product = domain + self.soup.find('a', attrs={'data-product-sku': product['id']})['href']
                self.products[index]['link'] = link_product
                MySQL().write_product(product=product, link_product=link_product, id_category=self.id_category)
            except:
                pass
        return self.products


if __name__ == '__main__':
    pass

