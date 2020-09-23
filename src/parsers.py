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
    domain = 'https://rabota.ua'
    resp = requests.get(url, headers=headers)
    jobs = []
    errors = []

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
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
    else:
        errors.append({'url': url, 'title': "Page do noot response"})
    return jobs, errors


if __name__ == '__main__':
    url = 'https://rabota.ua/zapros/python/%d1%83%d0%ba%d1%80%d0%b0%d0%b8%d0%bd%d0%b0'
    jobs, errors = rabota(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
