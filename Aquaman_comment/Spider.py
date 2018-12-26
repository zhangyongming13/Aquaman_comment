#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import requests
import codecs
import time
import random
from bs4 import BeautifulSoup


absolute  = 'https://movie.douban.com/subject/1292722/comments'
# absolute_url = 'https://movie.douban.com/subject/3878007/comments?start=20&limit=20&sort=new_score&status=P'
# url = 'https://movie.douban.com/subject/3878007/comments?start={}&limit=20&sort=new_score&status=P'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36', 'Connection':'keep-alive'}


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    comment_list = comment(html)
    if soup.select('#paginator > span') == []:
        next_page = soup.select('#paginator > a')[2].get('href')  # 表示根据tag的id是paginator进行检查
    else:
        next_page = []
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
    next_page = '?start=20&limit=20&sort=new_score&status=P&percent_type='
    while(next_page != []):
        print(absolute + next_page)
        zhang = absolute + next_page  # 拼接下一页的链接
        html = requests.get(zhang, cookies = cookies, headers = header).content  # 创建requests请求
        soup = BeautifulSoup(html, 'lxml')  # 使用lxml的解析器
        comment_list, next_page, date_node = get_data(html,)
        with open('Taitanic.txt', 'a', encoding = 'utf-8')as f:  # 写入文件
            for node in comment_list:
                yong = list(node)
                f.writelines(list(yong[0])[0] + list(yong[1])[0].strip() + u'\n')
        time.sleep(20 + float(random.randint(1, 100)) / 20)
