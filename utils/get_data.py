# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from config import run_proxy


def get_soup(url, method='get_content', timeout=600):
    try:
        data = {
            'method': method,
            'url': url,
            'timeout': timeout,
        }

        if run_proxy:
            response = requests.get(url='http://45.133.245.10/sjdfhsajdsjksdhfdsggsgeyeyey', params=data).json()['response']
        else:
            response = requests.get(url=url)
            response.encoding = 'utf-8'
            response = response.text

        return response, BeautifulSoup(response, 'html.parser')
    except:
        return False


if __name__ == '__main__':
    response = get_soup(url='https://goods.ru/catalog/details/pnevmaticheskiy-raspylitel-vysokogo-davleniya-szhatyy-vozduh-400ml-defender-cln30805-100023900749/')
    text = response[0].split('_GOODS_.catalog_page = ')[-1].split('_GOODS_.gaPushInitData = ')[0].strip().strip(';')
    soup = response[1]
    import json
    js = json.loads(text)
    products = dict(js)['items']
    for product in products:
        print(product)
