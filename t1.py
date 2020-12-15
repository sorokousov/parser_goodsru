from utils.get_data import get_soup
import json
from bs4 import BeautifulSoup
from config import sum_key
from utils.ftp import send_to_ftp


# descriptions_block = response[1].find('div', attrs={'id': 'pdp-description'}).find('div', attrs={'class': 'row'})
#
# desc1 = descriptions_block.find_all(['p', 'h2', 'li'])
# opis = 'Описание'
# txt = opis + '\n'
# try:
#     for tag in desc1:
#         tagtext = tag.text.strip()
#         if tag.name == 'li':
#             txt += '- ' + tagtext + '\n'
#         elif tag.name == 'p':
#             txt += tagtext + '\n\n'
#         elif tag.name == 'h2':
#             txt += '\n' + tagtext + '\n'
#         else:
#             txt += tag.text
#
#     if txt.strip() == opis:
#         cut_text = descriptions_block.find('div', attrs={'class': 'additional-descr'}).text.strip()
#         desc2 = descriptions_block.find('div', attrs={'itemprop': 'description'}).text.strip().replace(cut_text, '')
#         txt += desc2
#
#     if txt.strip() == opis:
#         txt = 'Нет описания'
# except:
#     txt = 'Нет описания'
#
# txt = txt.strip()
# print(txt)

def get_images(response, sku, id_category):

    component = response[1].find('component', attrs={'is': 'imageZoomSlider'})
    images = component.find_all('img')

    links_small = []
    for i in images:
        links_small.append(
            i['src'].replace('sml3', 'big2')
        )

    return links_small


if __name__ == '__main__':
    id_category = 20
    sku = str(100000404443 + sum_key)
    url = 'https://goods.ru/catalog/details/geympad-sony-dualshock-4-spartak-gladiator-100023216047/'
    response = get_soup(url=url)
    get_images(response=response, sku=sku, id_category=id_category)