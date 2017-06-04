import requests
from bs4 import BeautifulSoup
from song_singer.ConnectionException import ConnectionException
import re
import sys
import argparse


def parse_inquiry(inq):
    res = str.split(inq, ':')
    if len(res) != 2:
        print("Wrong input\nUsage: ./test Leonard Cohen : Hallelujah", file=sys.stderr)
        exit(-1)
    for i in range(len(res)):
        res[i] = res[i].strip(' ')

    return res


def safe_get(s):
    r = requests.get(s)
    r.encoding = 'utf-8'

    if r.status_code != 200:
        pass
        raise ConnectionException("Error while connecting to website '" + s + "'")
    return r


def get_titles_from_addr(address):
    raw_html = BeautifulSoup(safe_get(address).text, 'html.parser'). \
        findAll('div').__str__()

    tmp1 = re.search(r'Znalezione([\w\W]*?)30.(.*)', re.sub(re.compile('<.*?>'), '', raw_html)).group(0).split('\n')

    tmp2 = []
    for t in tmp1[1:]:
        if len(t) < 3:
            continue
        if not t.strip().startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            break
        tmp2.append(t)

    for i in range(len(tmp2)):
        tmp2[i] = tmp2[i].split('. ')[1].split(' - ')
        for j in range(len(tmp2[i])):
            tmp2[i][j] = tmp2[i][j].strip(' ')

    return tmp2


def remove_wrong_titles(alist, title):
    res = []
    for t in alist:
        if len(t) == 2 and t[1].lower() == title.lower():
            res.append(t)

    return res


def judge_truth(alist, author):
    res = False
    for t in alist:
        if t[0].lower() == author.lower():
            res = True
    return res


def unicode(s, *_):
    return s


if __name__ == '__main__':
    parser = argparse.ArgumentParser("test")
    parser.add_argument("sentence", nargs='+', type=lambda s: unicode(s, sys.getfilesystemencoding()),
                        help="Sentence to be checked for truth\nUsage: ./test Leonard Cohen : Hallelujah")
    arg = ' '.join(parser.parse_args().sentence)

    auth_title = parse_inquiry(arg)
    addr = "http://www.tekstowo.pl/szukaj,wykonawca," + auth_title[0].replace(' ', '+') + ",tytul," + auth_title[
        1].replace(' ', '+') + ".html"

    auth_title_list = get_titles_from_addr(addr)
    auth_title_list = remove_wrong_titles(auth_title_list, auth_title[1])

    print(auth_title[0] + (' is the author of ' if judge_truth(auth_title_list, auth_title[0])
                           else ' probably is not the author of ') + auth_title[1])
