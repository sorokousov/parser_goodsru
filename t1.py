# -*- coding: utf-8 -*-
from utils.get_data import get_soup
from utils.mysql_class import MySQL
from datetime import datetime
from time import sleep
from utils.ftp import send_to_ftp, save_to_disk


def get_images_two(response):
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
    response = get_soup(url='https://goods.ru/catalog/details/chaynik-elektricheskiy-endever-skyline-kr-335-g-600000756878/')

    images = get_images_two(response=response)
    print(images)


if __name__ == '__main__':
    main()

    exit()




