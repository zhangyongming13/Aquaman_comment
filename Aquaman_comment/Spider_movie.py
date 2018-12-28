#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import requests
import codecs
import time
import random
from bs4 import BeautifulSoup


absolute_url = 'https://movie.douban.com/top250'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find_all('ol', {'class':'grid_view'})
    next = soup.find('span', {'class':'next'})
    link = next.find('a')
    if link == None:
        next_page = None
    else:
        next_page = link['href']
    movie = []
    for data in body:
        zhang = []
        # print(len(data))
        for i in range(0, len(data) - 2):
            name = data.find_all('span', {'class':'title'})[i].strings
            zhang.append(name)
            # print(zhang)
        movie.append(zhang)
    return movie, next_page


if __name__ == '__main__':
    cookie = open('cookie.txt', 'r')
    cookies = {}
    for line in cookie.read().split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    next_page = '?start=0&filter='
    while(next_page != None):
        print(absolute_url + next_page)
        url = absolute_url + next_page
        html = requests.get(url, cookies, headers = header).content
        name, next_page = get_data(html)
        flag = 0
        with open('movie_name.txt', 'a', encoding='utf-8') as f:
            for data in name:
                zhang = list(data)
                for data_1 in zhang:
                    yong = list(data_1)[0]
                    if re.match(r'\s/\s\w*', yong):
                        pass
                    else:
                        if flag == 0:
                            flag = 1
                        else:
                            f.writelines(u'\n')
                    yong = yong.replace('/', '')
                    f.writelines(yong)
        # print(next_page)
        time.sleep(3 + float(random.randint(1, 100)) / 20)
    print('爬取完毕！')
