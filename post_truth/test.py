import requests
from bs4 import BeautifulSoup
from post_truth.ConnectionException import ConnectionException
import re
import sys
import argparse

# from google import search



def safe_get(s):
    r = requests.get(s)

    if r.status_code != 200:
        raise ConnectionException("Error while connecting to website '" + s + "'")
    return r


def get_titles_from_addr(addr):
    raw_html = BeautifulSoup(safe_get(addr).text, 'html.parser'). \
        findAll('div').__str__()
    tmp1 = re.search(r'Znalezione([\w\W]*?)10.(.*)',
                    re.sub(re.compile('<.*?>'), '', raw_html)).group(0).split('\n')

    tmp2 = []
    for t in tmp1[1:]:
        if len(t) > 3:
            tmp2.append(t)

    for i in range(len(tmp2)):
        tmp2[i]=tmp2[i].split('. ')[1].split(' - ')
        for j in range(len(tmp2[i])):
            tmp2[i][j]=tmp2[i][j].strip(' ')



    return tmp2


def parse_inquiry(inq):
    res=str.split(inq,':')
    if len(res)!=2:
        print("Wrong input\nUsage: ./test Leonard Cohen : Hallelujah",file=sys.stderr)
        exit(-1)
    for i in range(len(res)):
        res[i]=res[i].strip(' ')
    print(res)
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser("test")
    parser.add_argument("sentence", nargs='+',help="Sentence to be checked for truth\nUsage: ./test Leonard Cohen : Hallelujah")
    arg = ' '.join(parser.parse_args().sentence)

    # print(args)
    parse_inquiry(arg)
    # auth_title=parse_inquiry('Ariana Grande : Hallelujah')


# addr = "http://www.tekstowo.pl/szukaj,wykonawca,,tytul,"
#
#
# adr = "http://www.tekstowo.pl/szukaj,wykonawca,,tytul,shape+of+you.html"
#
# print(get_titles_from_addr(adr))
