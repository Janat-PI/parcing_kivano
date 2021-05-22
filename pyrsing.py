from bs4 import BeautifulSoup
import requests
import csv
import lxml
from multiprocessing import Pool
import json

def get_html(url):
    response = requests.get(url)
    # print(response.status_code)
    return response.text


def get_page_number(html):
    soup = BeautifulSoup(html, 'lxml')
    page_list = soup.find('div', class_='pager-wrap').find('ul', class_='pagination').find_all('li')
    page = page_list[-1].text
    page = int(page)
    return page

def write_to_csv(data):
    with open('parsing_nooteBooks.csv', 'a') as file:
        try:
            writer = csv.writer(file)
            writer.writerow((data['title'],
                            data['price']))
        except Exception as e:
            print(f'it is error {e}')

def write_to_json(data):
    with open('info.json', 'a') as file:
        json.dump(data, file)


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_='product-index').find('div', class_='list-view').find_all('div', class_='item')
    for product in product_list:
        try:
            title = product.find('div', class_='listbox_title').find('strong').text
            title = title.lstrip()
            letter = ['С', 'К', 'Р', '"', 'П', 'Ч', 'М']
            if title[0] in letter:
                continue
            # print(title)
        except:
            title = ""
        # try:
        #     description = product.find('div', class_='product_text').text
        #     description = description.strip() 
        #     print(description)
        # except:
        #     description = ""
        try:
            price = product.find('div', class_='listbox_price').find('strong').text
            price = int(price.replace('сом', ''))
            if price > 35000 and price < 58000:
                price = price
            else:
                price = ''
        except:
            price = ""
        dict_ = {'title': title, 'price': price}

        write_to_csv(dict_)
        write_to_json(dict_)
        

def speed_up(url):
    html = get_html(url)
    data = get_page_data(html)



def main():
    url = 'https://www.kivano.kg/noutbuki-i-kompyutery'
    page = '?page='
    html = get_html(url)
    number = get_page_number(html)
    urls = [url + page + str(i) for i in range(1,  number + 1)]
    with Pool(100) as p:
        p.map(speed_up, urls)
    # for i in range(1, number + 1):
    #     url_with_page = url + page + str(i)
    #     html = get_html(url_with_page)
    #     get_page_data(html)

if __name__ == '__main__':
    main()