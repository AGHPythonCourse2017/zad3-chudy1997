import mock
import pytest
from song_singer.main import parse_inquiry, safe_get, \
    ConnectionException, remove_wrong_titles, \
    judge_truth, get_titles_from_addr, check


def test_parse_inquiry_pos(capsys):
    parse_inquiry('Hans Zimmer : Tennessee')
    out, err = capsys.readouterr()
    assert err == ''


def test_parse_inquiry_neg(capsys):
    res = parse_inquiry('Hans Zimmer Tennessee')
    out, err = capsys.readouterr()
    assert err == "Wrong input\nUsage: main.check('Leonard Cohen : " \
                  "Hallelujah')\n" and res is None


def test_safe_get():
    with pytest.raises(ConnectionException):
        safe_get('https://pypi.python.org/pipy')
    assert safe_get('https://pypi.python.org/pypi') is not None


@mock.patch('song_singer.main.safe_get')
def test_get_titles_from_addr_pos(mock_get):
    with open('ex1.html', 'r') as f:
        mock_get.return_value = f.read()
    assert get_titles_from_addr('lalala') != []


@mock.patch('song_singer.main.safe_get')
def test_get_titles_from_addr_neg(mock_get):
    with open('ex2.html', 'r') as f:
        mock_get.return_value = f.read()
    assert get_titles_from_addr('lalala') == []


def test_remove_wrong_titles():
    assert remove_wrong_titles(
        [['Hallelujah'], ['Leonard Cohen'], ['Leonard Cohen', 'Hallelujah'],
         ['Leonard Cohen', 'Alleluja']], 'Hallelujah') == \
           [['Leonard Cohen', 'Hallelujah']]


def test_judge_truth_pos():
    assert judge_truth([['Lady Pank', 'Kryzysowa Narzeczona']], 'Lady Pank')


def test_judge_truth_neg():
    assert not judge_truth([['Metallica', 'Nothing else matters'],
                            ['Sunga Jung', 'Nothing else matters']], 'Adele')


@mock.patch('song_singer.main.get_titles_from_addr')
def test_check_pos(mock_check, capsys):
    mock_check.return_value = [['Three Days Grace', 'Animal i have become'],
                               ['Three Days Grace', 'Everything about you']]

    check('Three Days Grace : Animal I have become')
    out, err = capsys.readouterr()
    assert out == 'Three Days Grace sings Animal I have become\n'


@mock.patch('song_singer.main.get_titles_from_addr')
def test_check_neg(mock_check, capsys):
    mock_check.return_value = [['Metallica', 'Wherever I may roam'],
                               ['Metallica', 'Am I devil?']]

    check('Metallica : Animal I have become')
    out, err = capsys.readouterr()
    assert out == 'Metallica probably doesn\'t sing Animal I have become\n'
