# -*- coding: utf-8 -*-
from utils.get_data import get_soup
from classes.product_list import ProductList
from utils.mysql_class import MySQL
import threading
from datetime import datetime

thread_active = 3


def get_products_from_category(category):
    if category['links'].endswith('/'):
        page_link = category['links']
    else:
        page_link = category['links'] + '/'

    for n in range(1, 100000):

        if n > 1:
            link = page_link + f"page-{n}/"
        else:
            link = page_link
        print('Page', link)
        pl = ProductList(page_link=link, id_category=category['categories_5'])

        if not pl.this_is_404_page:
            if pl.this_is_product_list:
                if pl.contains_product:
                    pl.get_and_write_products()
                else:
                    MySQL().set_category_ready(id_category=category['id'])
                    print('Category', category['id'], 'READY NOT PRODUCTS')
                    break
            else:
                MySQL().set_category_bad(id_category=category['id'])
                print('Category', category['id'], 'BAD')
                break
        else:
            MySQL().set_category_ready(id_category=category['id'])
            print('Category', category['id'], 'READY 404')
            break


def main():
    start_time = datetime.now()

    while True:
        categories = MySQL().get_categories()
        count_category = len(categories)

        if count_category > 0:
            category = categories[0]

            MySQL().set_category_in_process(id_category=category['id'])
            print('----->', datetime.now() - start_time)
            print('Get category', category['categories_5'], 'from', count_category, category['links'])

            get_products_from_category(category)


if __name__ == '__main__':
    main()



    exit()




