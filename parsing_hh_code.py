import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import json

def get_vacancies():
    
   
    headers_gen = Headers(os="win", browser="chrome")
    
    url_main = "https://spb.hh.ru/search/vacancy?area=2&area=1&enable_snippets=true&order_by=publication_time&ored_clusters=true&text=python&search_period=1"
    
    response = requests.get(url_main, headers=headers_gen.generate())
    soup = BeautifulSoup(response.text, "lxml")

    
    vacancies = []
    
    vacancys_list = soup.find("main", class_="vacancy-serp-content")
    
    vacancys_tags = vacancys_list.find_all("div", class_="vacancy-serp-item__layout")
    
    for vacancy in vacancys_tags:
        vac = vacancy
        link_vacancy = vacancy.find("a", class_="serp-item__title").get("href")
     
        salary = vacancy.find(
            "span", class_="bloko-header-section-2", attrs={
            "data-qa": "vacancy-serp__vacancy-compensation"
            }
            )
        if salary is not None:
            salary = salary.text.strip()
        company = vacancy.find("div", class_="vacancy-serp-item__meta-info-company").text.strip()
        # я не понимаю как вывести только город, поэтому вывожу все
        city = vacancy.find(
            "div", class_="bloko-text", attrs={
            "data-qa": "vacancy-serp__vacancy-address"
            }
            ).text.strip('')
        
        article_full_html = requests.get(link_vacancy, headers=headers_gen.generate()).text
        article_soup = (BeautifulSoup(article_full_html, "lxml"))
        
        article_full_soup = article_soup.find("div", class_="vacancy-section")
      
        if "Django" in article_full_soup.text or "Flask" in article_full_soup.text:
            vacancy_data = {
                "link": link_vacancy,
                "salary": salary,
                "company": company,
                "city": city
            }
            vacancies.append(vacancy_data)
 
    return vacancies

vacancies = get_vacancies()
import json
with open("vacancies.json", "w", encoding="utf-8") as file:
    json.dump(vacancies, file, ensure_ascii=False, indent=4)