# -*- coding: utf-8 -*-
from ftplib import FTP
import socket
from config import sum_key
import requests
import os
import pysftp


def save_to_disk(files, id_category, sku):
    root_dir = './goodsru'
    sku = f"{sku + sum_key}"
    sku_dir = f"/{sku}"
    category = f"{id_category}"
    category_dir = f"/{category}"
    dir = root_dir + category_dir + sku_dir


    if not os.path.lexists(dir):
        try:
            os.mkdir(root_dir)
        except:
            pass

        try:
            os.mkdir(root_dir + category_dir)
        except:
            pass

        try:
            os.mkdir(root_dir + category_dir + sku_dir)
        except:
            pass

    result = []
    for index, file in enumerate(files, start=1):
        try:
            path = f"{dir}/{sku}_{index}.jpg"
            res_file = requests.get(url=file, stream=True)
            if res_file.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in res_file:
                        f.write(chunk)

            result.append({'sku': int(sku), 'path': path, 'link': file})
        except:
            result = False
            break

    return result


def send_to_ftp(files, id_category, sku):
    root_dir = '/goodsru'
    sku = f"{sku + sum_key}"
    sku_dir = f"/{sku}"
    category = f"{id_category}"
    category_dir = f"/{category}"
    dir = root_dir + category_dir + sku_dir

    host_ftp = '5.180.136.10'
    user_ftp = 'user1924153'
    password_ftp = 'aEdAsHaXnne9'

    try:
        ftp = FTP(host_ftp)
        ftp.login(user=user_ftp, passwd=password_ftp)
        ftp.set_pasv(False)
    except:
        print('ERROR CONNECTING FTP')
        return False

    try:
        ftp.cwd(dir)
    except:

        try:
            ftp.mkd(root_dir)
        except:
            pass

        try:
            ftp.cwd(root_dir)
            ftp.mkd(category)
        except:
            pass

        try:
            ftp.cwd(root_dir + category_dir)
            ftp.mkd(sku)
        except:
            pass

        try:
            ftp.cwd(root_dir + category_dir + sku_dir)
        except:
            return False

    result = []
    for index, link in enumerate(files, start=1):
        try:
            res_file = requests.get(url=link, stream=True)
            if res_file.status_code == 200:
                with open('tmp.tmp', 'wb') as f:
                    for chunk in res_file:
                        f.write(chunk)

            path = f"{dir}/{sku}_{index}.jpg"
            res_file = open('tmp.tmp', 'rb')
            ftp.storbinary('STOR ' + path, res_file, 1024)
            result.append([int(sku), path, link])
        except:
            result = False
            break

    ftp.close()
    return result


if __name__ == '__main__':
    id_category = 214244
    sku = 12334253444
    files = ['https://main-cdn.goods.ru/big2/hlr-system/1605073/100023216047b0.jpg', 'https://main-cdn.goods.ru/big2/hlr-system/1605074/100023216047b1.jpg', 'https://main-cdn.goods.ru/big2/hlr-system/1605075415/100023216047b2.jpg', 'https://main-cdn.goods.ru/big2/hlr-system/1605076415/100023216047b3.jpg', 'https://main-cdn.goods.ru/big2/hlr-system/1605077415/100023216047b4.jpg', 'https://main-cdn.goods.ru/big2/hlr-system/1605078415/100023216047b5.jpg', 'https://main-cdn.goods.ru/big2/hlr-system/1605079415/100023216047b6.jpg', 'https://main-cdn.goods.ru/big2/hlr-system/1605080415/100023216047b7.jpg']
    s = send_to_ftp(files=files, id_category=id_category, sku=sku)
    print(s)