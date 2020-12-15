# -*- coding: utf-8 -*-
from config import sum_key
from mysql.connector import MySQLConnection
from contextlib import contextmanager
from datetime import datetime
import calendar
from config import db_config


@contextmanager
def connect_db():
    conn = MySQLConnection(host=db_config['host'], user=db_config['user'], password=db_config['password'])
    try:
        conn.database = db_config['database']
        yield conn.cursor(dictionary=True)
    finally:
        try:
            conn.commit()
        finally:
            conn.close()


class MySQL:
    def write_db(self, query, data=None):
        with connect_db() as cursor:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)

    def read_db(self, query, data=None):
        with connect_db() as cursor:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            ret = cursor.fetchall()
            return ret

    # product_list

    def get_categories(self):
        try:
            return self.read_db('select * from categories where status_products="stop"', ())
        except:
            return None

    def set_category_ready(self, id_category):
        self.write_db('update categories set status_products="ready" where id=%s', (id_category,))

    def set_category_stop(self, id_category):
        self.write_db('update categories set status_products="stop" where id=%s', (id_category,))

    def set_category_bad(self, id_category):
        self.write_db('update categories set status_products="bad" where id=%s', (id_category,))

    def set_category_in_process(self, id_category):
        self.write_db('update categories set status_products="in_process" where id=%s', (id_category,))

    def write_product(self, product, link_product, id_category):
        if product['price'] >= 7000:
            price = product['price']
        elif product['price_last'] >= 7000:
            price = product['price_last']
        else:
            return None

        try:
            id_brand = self.read_db('select id from brands where name=%s', (product['brand'],))[0]['id']
        except:
            self.write_db('insert into brands(name) values(%s)', (product['brand'],))
            id_brand = self.read_db('select id from brands where name=%s', (product['brand'],))[0]['id']

        try:
            self.write_db(query='insert into products(sku,price,name,id_brand,id_category,link_product,date_update) values(%s,%s,%s,%s,%s,%s,%s)',
                          data=(product['id'], price, product['name'], id_brand, id_category, link_product, datetime.now()))
        except:
            print('DUPLICATE')

        return True

    # image + description

    def get_product_main(self):
        try:
            return self.read_db('select * from products where status_images="stop" limit 1', ())[0]
        except:
            return None

    def set_product_main_in_process(self, id_product):
        self.write_db('update products set status_images="in_process" where id=%s', (id_product,))

    def set_product_main_ready(self, id_product):
        self.write_db('update products set status_images="ready" where id=%s', (id_product,))

    def set_product_main_stop(self, id_product):
        self.write_db('update products set status_images="stop" where id=%s', (id_product,))

    def set_product_main_bad(self, id_product):
        self.write_db('update products set status_images="bad" where id=%s', (id_product,))

    def write_images(self, images):
        for image in images:
            try:
                self.write_db(query='insert into images(sku,path) values(%s,%s)',
                              data=(image['sku'], image['path']))
            except:
                pass

    def write_description(self, sku, description):
        try:
            self.write_db(query='insert into descriptions(sku,description) values(%s,%s)',
                          data=(sku, description))
        except:
            pass

    # spec

    def get_product_spec(self):
        try:
            return self.read_db('select * from products where status_specifications="stop" limit 1', ())[0]
        except:
            return None

    def set_product_spec_in_process(self, id_product):
        self.write_db('update products set status_specifications="in_process" where id=%s', (id_product,))

    def set_product_spec_ready(self, id_product):
        self.write_db('update products set status_specifications="ready" where id=%s', (id_product,))

    def set_product_spec_stop(self, id_product):
        self.write_db('update products set status_specifications="stop" where id=%s', (id_product,))

    def set_product_spec_bad(self, id_product):
        self.write_db('update products set status_specifications="bad" where id=%s', (id_product,))

    def write_spec(self, sku, spec):

        rgs_str = ','.join(['({},"{}","{}")'.format(sku, i["name"], i["value"]) for i in spec])
        self.write_db(query=('insert into specifications (sku,name,value) values' + rgs_str), data=())


if __name__ == '__main__':
    a = [{'name': 'Бренд', 'param': 'ATLANT'}, {'name': 'Модель', 'param': 'ХМ 6021-031'}, {'name': 'Артикул производителя', 'param': '101508'}, {'name': 'Вид', 'param': 'отдельностоящий'}, {'name': 'Тип', 'param': 'двухкамерный'}, {'name': 'Количество камер', 'param': '2'}, {'name': 'Количество дверей', 'param': '2'}, {'name': 'Расположение морозильной камеры', 'param': 'снизу'}, {'name': 'Общий объем, в литрах', 'param': '345'}, {'name': 'Система No Frost', 'param': 'без No Frost'}, {'name': 'Климатический класс', 'param': 'SN-ST'}, {'name': 'Компрессор', 'param': 'стандартный'}, {'name': 'Количество компрессоров', 'param': '2'}, {'name': 'Уровень шума, в децибелах', 'param': '40'}, {'name': 'Класс энергоэффективности', 'param': 'A'}, {'name': 'Энергопотребление, в кВт*ч/год', 'param': '374'}, {'name': 'Объем холодильной камеры, в литрах', 'param': '225'}, {'name': 'Размораживание холодильной камеры', 'param': 'капельная система'}, {'name': 'Зона свежести', 'param': 'Нет'}, {'name': 'Объем морозильной камеры, в литрах', 'param': '101'}, {'name': 'Класс морозильной камеры', 'param': '***'}, {'name': 'Минимальная температура в морозильной камере, в °C', 'param': '-18'}, {'name': 'Размораживание морозильной камеры', 'param': 'ручное'}, {'name': 'Мощность замораживания, килограммов в сутки', 'param': '15'}, {'name': 'Сохранение холода при отключении питания, в часах', 'param': '17'}, {'name': 'Количество секций морозильной камеры', 'param': '1'}, {'name': 'Особенности конструкции', 'param': 'перенавешиваемые двери; ручки легкого открывания'}, {'name': 'Материал корпуса', 'param': 'металл'}, {'name': 'Цвет корпуса', 'param': 'белый'}, {'name': 'Дисплей', 'param': 'отсутствует'}, {'name': 'Тип управления', 'param': 'электромеханическое'}, {'name': 'Режимы работы', 'param': 'суперзаморозка'}, {'name': 'Индикация', 'param': 'режима работы; открытой двери холодильной камеры'}, {'name': 'Количество полок в холодильной камере', 'param': '4'}, {'name': 'Количество ящиков в холодильной камере', 'param': '2'}, {'name': 'Количество полок на двери холодильной камеры', 'param': '6'}, {'name': 'Количество ящиков в морозильной камере', 'param': '3'}, {'name': 'Комплект поставки', 'param': 'формочки для льда; кронштейн для бутылок; подставка для яиц'}, {'name': 'Высота, в сантиметрах', 'param': '186'}, {'name': 'Ширина, в сантиметрах', 'param': '60'}, {'name': 'Глубина, в сантиметрах', 'param': '63'}, {'name': 'Вес, в килограммах', 'param': '71'}, {'name': 'Габариты, в сантиметрах (ВxШxГ)', 'param': '186x60x63'}]
    MySQL().write_spec(sku=123, spec=a)