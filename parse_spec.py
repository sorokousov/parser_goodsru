# -*- coding: utf-8 -*-
from utils.get_data import get_soup
from utils.mysql_class import MySQL
from datetime import datetime
from time import sleep
from utils.ftp import send_to_ftp, save_to_disk


def get_spec(response):
    spec = []
    try:
        spec_blocks = response[1].find_all('table', attrs={'class': 'tbl-typical'})
        for block in spec_blocks:
            try:
                trs = block.find_all('tr')
                for tr in trs:
                    name = tr.find('td', attrs={'class': 'color-grey'}).text.strip()
                    param = tr.find('div', attrs={'class': 'attribute-value'}).text.strip()
                    spec.append({
                        'name': name,
                        'value': param
                    })
            except:
                pass
    except:
        pass

    return spec


def main():
    start_time = datetime.now()
    n = 0

    while True:
        product_ = MySQL().get_product_spec()
        MySQL().set_product_spec_in_process(id_product=product_['id'])

        link_ = product_['link_product']
        if link_.endswith('/'):
            link = link_ + 'spec/'
        else:
            link = link_ + '/spec/'

        response = get_soup(url=link)
        sku = product_['sku']
        id_product = product_['id']

        spec = get_spec(response=response)

        if spec:
            MySQL().write_spec(sku=sku, spec=spec)
        else:
            MySQL().set_product_spec_stop(id_product=id_product)

        n += 1
        print('\rCount', n, 'Time', datetime.now() - start_time, end='')
        sleep(0.5)


if __name__ == '__main__':
    main()


