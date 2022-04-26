from bs4 import BeautifulSoup
import re
import requests
import datetime
import csv

url_filter = re.compile(r'^https://www.abc.net.au/news/')
article_filter = re.compile(r'/news/\d{4}')
date_filter = re.compile(r'\d{4}-\d{2}-\d{2}')

headlines = []
article_links = []
dates = []


# generate a list to crawl through
def abc_get_links():
    html = requests.get('https://www.abc.net.au/news/')
    bsObj = BeautifulSoup(html.text,'lxml')

    abc_links = []
    for section in bsObj.find('ul',{'class':'ZJeip'}).children:
        for i in section:
            abc_links.append('https://www.abc.net.au'+i['href'])

    return abc_links


# pull page headlines, dates and links
def page_articles(url):
    html  = requests.get(url)
    bsObj = BeautifulSoup(html.text,'lxml')

    for i in bsObj.find_all('a'):
        # pull all articles
        if re.search(article_filter,i['href']) != None:
            if re.search(url_filter,i['href']) != None and i['href'] not in article_links:
                headlines.append(i.text)
                article_links.append(i['href'])
                date = re.search(date_filter,i['href']).group()
                dates.append(date)
            else:
                if 'https://www.abc.net.au/news'+i['href'] not in article_links:
                    headlines.append(i.text)
                    article_links.append('https://www.abc.net.au/news'+i['href'])
                    date = re.search(date_filter,i['href']).group()
                    dates.append(date)


# crawl through the tabs and pull headlines
def crawler():
    for i in abc_get_links():
        print(i)
        page_articles(i)


# run the crawler
crawler()

# write to csv
with open('abc_scrape.csv','w',newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Article','Date','Link'])
    for i in range(0,len(headlines)-1):
        try:
            writer.writerow([headlines[i],dates[i],article_links[i]])
        except UnicodeEncodeError:
            writer.writerow(['unicode_error','unicode_error'])
