# -*- coding: utf-8 -*-
from utils.get_data import get_soup
from utils.mysql_class import MySQL
from datetime import datetime
from time import sleep
from utils.ftp import send_to_ftp, save_to_disk


def get_images(response):

    try:
        component = response[1].find('component', attrs={'is': 'imageZoomSlider'})
        images = component.find_all('img')

        links_small = []
        for i in images:
            links_small.append(
                i['src'].replace('sml3', 'big2')
            )

        return links_small
    except:
        print('ERROR Images!')
        return False


def main():
    start_time = datetime.now()
    n = 0

    while True:
        product_ = MySQL().get_product_main()

        if product_:
            response = get_soup(url=product_['link_product'])
            sku = product_['sku']
            id_product = product_['id']
            id_category = product_['id_category']

            images = get_images(response=response)

            ftp_result = None
            if images:
                ftp_result = save_to_disk(files=images, sku=sku, id_category=id_category)

            if ftp_result:
                MySQL().write_images(images=ftp_result)
                MySQL().set_product_main_ready(id_product=id_product)
            elif ftp_result is False:
                MySQL().set_product_main_bad(id_product=id_product)
            else:
                MySQL().set_product_main_ready(id_product=id_product)

        n += 1
        print('\rCount', n, 'Time', datetime.now() - start_time, end='')
        # sleep(0.5)


if __name__ == '__main__':
    main()



    exit()




