# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from utils.get_data import get_soup
from utils.mysql_class import MySQL
from bs4 import BeautifulSoup

# git pull && apt install chromium-chromedriver -y && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && apt install ./google-chrome-stable_current_amd64.deb -y && pip3 install selenium


def get_reviews(sku, page_source):
    try:
        soup = BeautifulSoup(page_source, 'html.parser')
        reviews_divs = soup.find_all('div', attrs={'itemprop': 'review', 'itemtype': 'http://schema.org/Review'})

        rets = []
        for review_raw in reviews_divs:
            ret = [sku]

            try:
                name = review_raw.find('div', attrs={'class': 'sp-review-author-name'}).text.strip()
            except:
                name = ''
            if not name:
                break
            ret.append(name)

            try:
                date = review_raw.find('div', attrs={'class': 'sp-review-date'}).text.strip()
            except:
                date = ''
            ret.append(date)

            try:
                rating = review_raw.find('span', attrs={'class': 'sp-review-rating-value'}).text.strip()
            except:
                rating = ''
            ret.append(rating)

            try:
                plus = review_raw.find('div', attrs={'class': 'sp-review-pros-content sp-review-text-content'}).text.strip()
            except:
                plus = 'Нет'
            ret.append(plus)

            try:
                minus = review_raw.find('div', attrs={'class': 'sp-review-cons-content sp-review-text-content'}).text.strip()
            except:
                minus = 'Нет'
            ret.append(minus)

            try:
                comment = review_raw.find('div', attrs={'class': 'sp-review-body-content sp-review-text-content'}).text.strip()
            except:
                comment = 'Нет'
            ret.append(comment)

            rets.append(ret)
        return rets
    except:
        return False


def main():
    start_time = datetime.now()
    n = 0

    while True:
        sleep(5)
        print("Перезапуск браузера")

        chromeOptions = Options()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--no-sandbox')
        prefs = {"profile.managed_default_content_settings.images": 2}
        chromeOptions.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        # driver = webdriver.Chrome(options=chromeOptions)

        driver.get('https://www.w3.org/People/mimasa/test/')
        while True:
            try:
                product_ = MySQL().get_product_reviews()

                if product_:

                    sku = product_['sku']
                    id_product = product_['id']
                    id_category = product_['id_category']

                    # Преобразовываем URL
                    link_ = product_['link_product']
                    if link_.endswith('/'):
                        link = link_ + 'otzyvy/'
                    else:
                        link = link_ + '/otzyvy/'

                    # Забираем страницу и ждём окончания её загрузки
                    driver.get(link)
                    tmp = ''

                    while True:
                        page_source = driver.page_source
                        if len(page_source) > len(tmp):
                            tmp = page_source
                        else:
                            break

                    reviews = get_reviews(sku=sku, page_source=page_source)
                    # print(reviews)

                    if reviews:
                        MySQL().write_reviews(reviews=reviews)
                        MySQL().set_product_reviews_ready(id_product=id_product)
                    elif reviews is False:
                        MySQL().set_product_reviews_bad(id_product=id_product)
                    else:
                        MySQL().set_product_reviews_ready(id_product=id_product)

                    n += 1
                    print('\rCount', n, 'Time', datetime.now() - start_time, end='')
            except:
                break

        driver.close()
        driver.quit()

if __name__ == '__main__':
    main()