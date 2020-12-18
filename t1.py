from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime

options = Options()
options.headless = True

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

# driver = webdriver.Firefox(firefox_profile=firefox_profile, options=options)
driver = webdriver.Firefox(executable_path='./geckodriver', firefox_profile=firefox_profile, options=options)

driver.get('https://goods.ru/catalog/details/holodilnik-s-nizhney-morozilnoy-kameroy-indesit-itf-118-w-100023475679/otzyvy/')
tmp = ''
while True:
    page_source = driver.page_source
    if len(page_source) > len(tmp):
        tmp = page_source
    else:
        break


soup = BeautifulSoup(page_source, 'html.parser')
reviews_divs = soup.find_all('div', attrs={'itemprop': 'review', 'itemtype': 'http://schema.org/Review'})

rets = []
for review_raw in reviews_divs:
    ret = []

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
print(rets)
driver.close()
driver.quit()
