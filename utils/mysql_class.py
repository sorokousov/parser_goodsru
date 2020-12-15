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

    # product

    def get_product(self):
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





if __name__ == '__main__':
    MySQL().write_db(query='insert into products(sku,price,name,id_brand,id_category,link_product) values(%s,%s,%s,%s,%s,%s)',
                  data=('1111222333', 7689, 'STiralka', 7, 2, 'dskfhjsdf'))