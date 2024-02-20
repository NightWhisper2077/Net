from bs4 import BeautifulSoup

import requests


def html_sorter(html_class, soup):
    list = []
    mini_list = []

    for div in soup.find_all('div'):
        cls = div.get('class')

        if cls == html_class[0]:
            cur_price = div.find('b').text
            mini_list.append(f'{cur_price}')

            for _old in div.find_all('span'):
                if _old.get('class') is not None and _old.get('class')[0] == 'old-price':
                    mini_list.append(_old.text)

            list.append(mini_list.copy())
            mini_list.clear()
        elif cls == html_class[1]:
            mini_list.append(div.find('img').get('src'))

            name_class = ['catalog-card__title', 'cart-modal-title']
            for _name in div.find_all('a'):
                if _name.get('class') is not None and _name.get('class') == name_class:
                    mini_list.append(_name.text)

    return list


def writer(out, list, index):
    for _list in list:
        out.write(f'{index}, {_list[0]}, {_list[1]}, {_list[2]}, {_list[3]}\n')


def main():
    html_class = [['catalog-card__price-row'], ['catalog-card']]

    out = open('output.csv', 'w', encoding='utf-8')
    out.write(f'Number page, Name, Image, Current cost, Old cost\n')

    for i in range(12):
        resp = requests.get(f'https://biggeek.ru/catalog/apple-iphone?page={i}')

        html = resp.text

        bs = BeautifulSoup(html, "html.parser")

        result = html_sorter(html_class, bs)

        writer(out, result, i + 1)


main()
