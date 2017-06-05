import re
import sys

import requests
from bs4 import BeautifulSoup

from song_singer.ConnectionException import ConnectionException


def parse_inquiry(inq):
    res = str.split(inq, ':')
    if len(res) != 2:
        print("Wrong input\nUsage: main.check('Leonard Cohen : Hallelujah')",
              file=sys.stderr)
        return None
    return [elem.strip(' ') for elem in res]


def safe_get(s):
    r = requests.get(s)
    r.encoding = 'utf-8'

    if r.status_code != 200:
        raise ConnectionException("Error while connecting to website '" +
                                  s + "'")
    return r.text


def get_titles_from_addr(address):
    raw_html = BeautifulSoup(safe_get(address), 'html.parser'). \
        findAll('div').__str__()

    tmp1 = re.search(r'Znalezione([\w\W]*?)30.(.*)',
                     re.sub(re.compile('<.*?>'), '', raw_html))
    tmp1 = tmp1.group(0).split('\n')

    tmp2 = []
    for t in tmp1[1:]:
        if len(t) < 3:
            continue
        if not t.strip().startswith(tuple(str(i) for i in range(10))):
            break
        tmp2.append(t)

    for i in range(len(tmp2)):
        tmp2[i] = tmp2[i].split('. ')[1].split(' - ')
        for j in range(len(tmp2[i])):
            tmp2[i][j] = tmp2[i][j].strip(' ')

    return tmp2


def remove_wrong_titles(alist, title):
    return [elem for elem in alist if len(elem) == 2
            if elem[1].lower() == title.lower()]


def judge_truth(alist, author):
    for t in alist:
        if author.lower() in t[0].lower():
            return True
    return False


def unicode(s, *_):
    return s


def check(args):
    auth_title = parse_inquiry(args)
    if auth_title is None:
        return
    addr = "http://www.tekstowo.pl/szukaj,wykonawca," + \
           auth_title[0].replace(' ', '+') + ",tytul," + \
           auth_title[1].replace(' ', '+') + ".html"

    auth_title_list = get_titles_from_addr(addr)
    auth_title_list = remove_wrong_titles(auth_title_list, auth_title[1])
    if not auth_title_list:
        print(auth_title[0] + ' probably doesn\'t sing ' + auth_title[1])
        return

    print(auth_title[0] + (' sings '
                           if judge_truth(auth_title_list, auth_title[0])
                           else ' probably doesn\'t sing ') + auth_title[1])

    return
