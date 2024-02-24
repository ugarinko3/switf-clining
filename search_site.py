from bs4 import BeautifulSoup
import requests
from password import url_site
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                  'Safari/537.36'
}

""""  INFO IN  CLEANING  """

title_url = {}


def write_inf(data, file_name):
    data = json.dumps(data)
    data = json.loads(str(data))

    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def search(page):
    soup = BeautifulSoup(page, 'html.parser')

    # Service
    service = []
    info_service = []
    i = 0
    p_name_tags = soup.find_all('p', class_='textable css79')
    p_info_tags = soup.find_all('p', class_='textable css81')
    for tag_info in p_info_tags:
        info_service.append(tag_info.text)
    for tag in p_name_tags:
        list_time = [tag.text, info_service[i]]
        service.append(list_time)
        i += 1
    title_url['service'] = service

    # Minimal check
    info_min_price = []
    span_tags = soup.select('span', class_='textable css87')
    for i_title in span_tags:
        for a_tag in i_title:
            if 'от ' in a_tag:
                int_number = ''.join(c if c.isdigit() else ' ' for c in a_tag).split()
                num = int(int_number[0] + int_number[1])
                info_min_price.append(num)
    title_url['price'] = info_min_price

    # Info in cleaning
    span_info_tags = soup.find_all('p', class_='textable css152')
    info_company = []
    for i_span in span_info_tags:
        split_list = i_span.text.split(':')
        line_time = [split_list[0], split_list[1]]
        info_company.append(line_time)
    title_url['company'] = info_company


def start_search_site():
    search(requests.get(url_site).text)
    write_inf(title_url, "info_site/info_site.json")
