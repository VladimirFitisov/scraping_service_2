import requests
import codecs

from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0(Windows NT 5.1: rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }


def work(url):
    domain = 'https://www.work.ua'
    url = 'https://www.work.ua/jobs-python/'
    resp = requests.get(url, headers=headers)
    jobs = []
    errors = []

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='pjax-job-list')
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_list:
                title = div.find('h2')
                href = title.a['href']
                content = div.p.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
    else:
        errors.append({'url': url, 'title': "Page do noot response"})
    return jobs, errors


def rabota(url):
<<<<<<< HEAD
    domain = 'https://rabota.ua'
    resp = requests.get(url, headers=headers)
=======
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
        if not new_jobs:
            table = soup.find('table', id='ctl00_content_vacancyList_gridList')
            if table:
                tr_list = table.find_all('tr', attrs={'id': True})
                for tr in tr_list:
                    div = tr.find('div', attrs={'class': 'card-body'})
                    if div:
                        title = div.find('p', attrs={'class': 'card-title'})
                        href = title.a['href']
                        content = div.p.text
                        company = 'No name'
                        p = div.find('p', attrs={'class': 'company-name'})
                        if p:
                            company = p.a.text
                        jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
                    else:
                        errors.append({'url': url, 'title': "Table does not exists"})
            else:
                errors.append({'url': url, 'title': "Page is empty"})

    else:
        errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors


def dou(url):
    # domain = 'https://jobs.dou.ua/'
    # url = 'https://jobs.dou.ua/vacancies/?category=Python'
    resp = requests.get(url, headers=headers)
>>>>>>> c932f4d... Add new function Dou.ua end Djinni.ua
    jobs = []
    errors = []

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
<<<<<<< HEAD
        table = soup.find('table', id='ctl00_content_vacancyList_gridList')
        if table:
            tr_list = table.find_all('div', attrs={'id': True})
            for tr in tr_list:
                div = tr.find('div', attrs={'class': 'card-body'})
                if div:
                    title = div.find('p', attrs={'class': 'card-title'})
                    href = title.a['href']
                    content = div.p.text
                    company = 'No name'
                    p = div.find('div', attrs={'class': 'company-name'})
                    if p:
                        company = p.a.text
                    jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
                else:
                    errors.append({'url': url, 'title': "Table does not exists"})
=======
        main_div = soup.find('div', id='vacancyListId')
        if main_div:
            li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
            for li in li_list:
                title = li.find('div', attrs={'class': 'title'})
                href = title.a['href']
                cont = li.find('div', attrs={'class': 'sh-info'})
                content = cont.text
                company = 'No name'
                a = title.find('a', attrs={'class': 'company'})
                if a:
                    company = a.text
                cities = li.find('span', attrs={'class': 'cities'})
                if cities:
                    city = cities.text
                jobs.append({'title': title.text, 'url': href, 'description': content, 'company': company, 'city': city})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
>>>>>>> c932f4d... Add new function Dou.ua end Djinni.ua
    else:
        errors.append({'url': url, 'title': "Page do noot response"})
    return jobs, errors

<<<<<<< HEAD

if __name__ == '__main__':
    url = 'https://rabota.ua/zapros/python/%d1%83%d0%ba%d1%80%d0%b0%d0%b8%d0%bd%d0%b0'
    jobs, errors = rabota(url)
=======
def djinni(url):
    domain = 'https://djinni.co'
    # url = 'https://djinni.co/jobs/keyword-python/'
    resp = requests.get(url, headers=headers)
    jobs = []
    errors = []

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
        if main_ul:
            li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
            for li in li_list:
                title = li.find('div', attrs={'class': 'list-jobs__title'})
                href = title.a['href']
                cont = li.find('div', attrs={'class': 'list-jobs__description'})
                content = cont.text
                company = 'No name'
                comp = li.find('div', attrs={'class': 'list-jobs__details__info'})
                if comp:
                    company = comp.text
                cities = li.find('i', attrs={'class': 'icon-location'})
                if cities:
                    city = cities.text
                jobs.append({'title': title.text, 'url': domain+href, 'description': content, 'company': company, 'city': city})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
    else:
        errors.append({'url': url, 'title': "Page do noot response"})
    return jobs, errors



if __name__ == '__main__':
    url = 'https://djinni.co/jobs/keyword-python/'
    jobs, errors = djinni(url)
>>>>>>> c932f4d... Add new function Dou.ua end Djinni.ua
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
