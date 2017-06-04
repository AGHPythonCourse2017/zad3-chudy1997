from song_singer.main import *
import pytest


def test_parse_inquiry_pos(capsys):
    parse_inquiry('Hans Zimmer : Tennessee')
    out, err = capsys.readouterr()
    assert err == ''


def test_parse_inquiry_neg(capsys):
    res = parse_inquiry('Hans Zimmer Tennessee')
    out, err = capsys.readouterr()
    assert err == "Wrong input\nUsage: main.check('Leonard Cohen : Hallelujah')\n" and res is None


def test_safe_get():
    with pytest.raises(ConnectionException):
        safe_get('https://pypi.python.org/pipy')
    assert safe_get('https://pypi.python.org/pypi') is not None


def test_get_titles_from_addr_pos():
    def get_titles_from_addr_mock(address):
        with open('ex2.html', 'r') as f:
            raw_html = BeautifulSoup(f.read(), 'html.parser'). \
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

    assert get_titles_from_addr_mock('') == []


def test_get_titles_from_addr_neg():
    def get_titles_from_addr_mock(address):
        with open('ex1.html', 'r') as f:
            raw_html = BeautifulSoup(f.read(), 'html.parser'). \
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

    assert get_titles_from_addr('') != []


def test_remove_wrong_titles():
    assert remove_wrong_titles(
        [['Hallelujah'], ['Leonard Cohen'], ['Leonard Cohen', 'Hallelujah'], ['Leonard Cohen', 'Alleluja']],
        'Hallelujah') == [['Leonard Cohen', 'Hallelujah']]


def test_judge_truth_pos():
    assert judge_truth([['Lady Pank', 'Kryzysowa Narzeczona']], 'Lady Pank')


def test_judge_truth_neg():
    assert not judge_truth([['Metallica', 'Nothing else matters'], ['Sunga Jung', 'Nothing else matters']], 'Adele')


def test_check_pos(capsys):
    def check_mock(args):
        auth_title = parse_inquiry(args)
        if auth_title is None:
            return
        auth_title_list=[['Three Days Grace','Animal i have become'],['Three Days Grace','Everything about you']]
        auth_title_list = remove_wrong_titles(auth_title_list, auth_title[1])
        if not auth_title_list:
            print(auth_title[0] + ' probably doesn\'t sing ' + auth_title[1])
            return

        print(auth_title[0] + (' sings '
                               if judge_truth(auth_title_list, auth_title[0])
                               else ' probably doesn\'t sing ') + auth_title[1])

        return

    check('Three Days Grace : Animal I have become')
    out, err = capsys.readouterr()
    assert out == 'Three Days Grace sings Animal I have become\n'

def test_check_neg(capsys):
    def check_mock(args):
        auth_title = parse_inquiry(args)
        if auth_title is None:
            return
        auth_title_list=[['Metallica','Wherever I may roam'],['Metallica','Am I devil?']]
        auth_title_list = remove_wrong_titles(auth_title_list, auth_title[1])
        if not auth_title_list:
            print(auth_title[0] + ' probably doesn\'t sing ' + auth_title[1])
            return

        print(auth_title[0] + (' sings '
                               if judge_truth(auth_title_list, auth_title[0])
                               else ' probably doesn\'t sing ') + auth_title[1])

        return

    try:
        check('Metallica : Animal I have become')
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert out == 'Metallica probably doesn\'t sing Animal I have become\n'


