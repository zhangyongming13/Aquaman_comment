#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import requests
import codecs
import time
import random
from bs4 import BeautifulSoup


absolute  = 'https://movie.douban.com/subject/3878007/comments'
absolute_url = 'https://movie.douban.com/subject/3878007/comments?start=0&limit=20&sort=new_score&status=P'
url = 'https://movie.douban.com/subject/3878007/comments?start={}&limit=20&sort=new_score&status=P'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36', 'Connection':'keep-alive'}


def get_data(html):
    body = BeautifulSoup(html, 'lxml')
    comment_list = body.select('.comment > p')
    next_page = body.select('.paginator > a')[2].get('href')
    date_node = body.select('..comment-time')
    return comment_list, next_page, date_node


if __name__ == '__main__':
    f_cookies = open('cookies.txt', 'r')
    cookies = {}
    for line in f_cookies.read().split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value

    html = requests.get(absolute_url, cookies = cookies, header = header).content
    comment_list = []
    comment_list, next_page, date_node = get_data(html,)
    soup = BeautifulSoup(html, 'lxml')
    comment_list = []
    while(next_page != []):
        print(absolute + next_page)
        html = requests.get(absolute_url, cookies = cookies, header = header).content
        soup = BeautifulSoup(html, 'lxml')
        comment_list, next_page, date_node = get_data(html)
        with open('comment.txt', 'a', encoding = 'utf-8')as f:
            for node in comment_list:
                comment = node.get_text().strip().replace("\n", "")
                for date in date_node:
                    date = node.get_text().strip()
                    f.writelines((comment, date) + u'\n')
        time.sleep(1 + float(random.randint(1, 100)) / 20)
