#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import requests
import codecs
import time
import random
from bs4 import BeautifulSoup


absolute  = 'https://movie.douban.com/subject/3878007/comments'
absolute_url = 'https://movie.douban.com/subject/3878007/comments?start=20&limit=20&sort=new_score&status=P'
url = 'https://movie.douban.com/subject/3878007/comments?start={}&limit=20&sort=new_score&status=P'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36', 'Connection':'keep-alive'}


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    comment_list = comment(html)
    next_page = soup.select('#paginator > a')[2].get('href')
    date_node = soup.select('..comment-time')
    return comment_list, next_page, date_node


def comment(html):
    bs = BeautifulSoup(html, 'html.parser')
    body = bs.body
    data = body.find_all('div', {'class':'comment-item'})
    final = []
    for comment in data:
        data = []
        com = comment.find('span', {'class':'short'}).strings
        dat = comment.find('span', {'class':'comment-time'}).strings
        # print(com)
        data.append(com)
        data.append(dat)
        final.append(data)
    return final


if __name__ == '__main__':
    f_cookies = open('cookie.txt', 'r')
    cookies = {}
    for line in f_cookies.read().split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value

    # html = requests.get(absolute_url, cookies = cookies, headers = header).content
    # comment_list = []
    # comment_list, next_page, date_node = get_data(html,)
    # soup = BeautifulSoup(html, 'lxml')
    # comment_list = []
    next_page = '?start=20&limit=20&sort=new_score&status=P&percent_type='
    while(next_page != []):
        print(absolute + next_page)
        zhang = absolute + next_page
        html = requests.get(zhang, cookies = cookies, headers = header).content
        soup = BeautifulSoup(html, 'lxml')
        comment_list, next_page, date_node = get_data(html,)
        # print(comment_list)
        # print(next_page)
        # print(date_node)
        with open('comment.txt', 'a', encoding = 'utf-8')as f:
            for node in comment_list:
                # print(node)
                # comment = node.get_text().strip().replace("\n", "")
                # print(comment)
                yong = list(node)
                # for date in date_node:
                    # ming = list(date)
                    # print(ming[0])
                    # time.sleep(3)
                    # f.writelines(yong[0] + ming[0] + u'\n')
                    # print(yong[0])
                # for date in date_node:
                #     date = date.get_text().strip()
                # print(list(yong[0])[0])
                # print(list(yong[1])[0].strip())
                f.writelines(list(yong[0])[0] + list(yong[1])[0].strip() + u'\n')
        time.sleep(1 + float(random.randint(1, 100)) / 20)
