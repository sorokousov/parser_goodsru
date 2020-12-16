# -*- coding: utf-8 -*-
from utils.get_data import get_soup
from utils.mysql_class import MySQL
from datetime import datetime
from time import sleep
from utils.ftp import send_to_ftp, save_to_disk

thread_active = 3


def get_description(response):
    try:
        descriptions_block = response[1].find('div', attrs={'id': 'pdp-description'}).find('div', attrs={'class': 'row'})

        desc1 = descriptions_block.find_all(['p', 'h2', 'li'])
    except:
        print('Pizda s opisaniem!')
        return False
    opis = 'Описание'
    txt = opis + '\n'
    try:
        for tag in desc1:
            tagtext = tag.text.strip()
            if tag.name == 'li':
                txt += '- ' + tagtext + '\n'
            elif tag.name == 'p':
                txt += tagtext + '\n\n'
            elif tag.name == 'h2':
                txt += '\n' + tagtext + '\n'
            else:
                txt += tag.text

        if txt.strip() == opis:
            cut_text = descriptions_block.find('div', attrs={'class': 'additional-descr'}).text.strip()
            desc2 = descriptions_block.find('div', attrs={'itemprop': 'description'}).text.strip().replace(cut_text, '')
            txt += desc2

        if txt.strip() == opis:
            txt = 'Нет описания'
    except:
        txt = 'Нет описания'

    return txt.strip()


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
        # print('----------------->>>')
        # print(product_['sku'])
        # MySQL().set_product_main_in_process(id_product=product_['id'])

        response = get_soup(url=product_['link_product'])
        sku = product_['sku']
        id_product = product_['id']
        id_category = product_['id_category']

        description = get_description(response=response)
        # images = get_images(response=response)

        result = True
        ftp_result = None
        # if images:
        #     ftp_result = save_to_disk(files=images, sku=sku, id_category=id_category)
        # if images is False:
        #     result = False

        if result and description:
            # print('IF')
            if ftp_result:
                MySQL().write_images(images=ftp_result)
            MySQL().write_description(sku=sku, description=description)
            MySQL().set_product_main_ready(id_product=id_product)
        else:
            # print('ELSE')
            MySQL().set_product_main_ready(id_product=id_product)
            # MySQL().set_product_main_bad(id_product=id_product)

        n += 1
        print('\rCount', n, 'Time', datetime.now() - start_time, end='')
        sleep(0.5)


if __name__ == '__main__':
    main()



    exit()




