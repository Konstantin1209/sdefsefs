import bs4
import requests
import re
from fake_headers import Headers
import json


def get_fake_headers():
    return Headers( browser="chrome", os="win").generate()

def response_text():
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    response = requests.get(url, headers=get_fake_headers())
    main_page_data = bs4.BeautifulSoup(response.text, features='lxml')
    articles_list = main_page_data.find_all(class_='vacancy-serp-item__layout')
    result = []
    for article in articles_list:
        link = article.find('a')['href']
        salary = article.find('span', class_='bloko-header-section-3')
        company = article.find('a', class_='bloko-link bloko-link_kind-tertiary').text
        city = article.find('div',{'data-qa':'vacancy-serp__vacancy-address'}).text

        article_response = requests.get(link, headers=get_fake_headers())
        article_data = bs4.BeautifulSoup(article_response.text, features='lxml')
        article_text = article_data.find(class_='g-user-content')
        regex = r"Django|Flask"
        matches = re.findall(regex, str(article_text), re.MULTILINE)
        if len(matches)>0:
            info = {
                'link':link,
                'salary': salary,
                'company': company,
                'city': city   
                }
            result.append(info)
    
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
    
   

if __name__ == '__main__':
    response_text()
