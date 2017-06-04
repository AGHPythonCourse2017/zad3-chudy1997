from song_singer.main import *
import pytest


def test_parse_inquiry(capsys):
    parse_inquiry('Hans Zimmer : Tennessee')
    out, err = capsys.readouterr()
    assert err == ''
    res = parse_inquiry('Hans Zimmer Tennessee')
    out, err = capsys.readouterr()
    assert err == "Wrong input\nUsage: main.check('Leonard Cohen : Hallelujah')\n" and res is None


def test_safe_get():
    with pytest.raises(ConnectionException):
        safe_get('https://pypi.python.org/pipy')
    assert safe_get('https://pypi.python.org/pypi') is not None


def test_get_titles_from_addr():
    assert get_titles_from_addr('http://www.tekstowo.pl/szukaj,wykonawca,Garek,tytul,Iconers.html') == []
    assert get_titles_from_addr('http://www.tekstowo.pl/szukaj,wykonawca,Garek,tytul,Icon.html') != []


def test_remove_wrong_titles():
    assert remove_wrong_titles(
        [['Hallelujah'], ['Leonard Cohen'], ['Leonard Cohen', 'Hallelujah'], ['Leonard Cohen', 'Alleluja']],
        'Hallelujah') == [['Leonard Cohen', 'Hallelujah']]


def test_judge_truth():
    assert judge_truth([['Lady Pank', 'Kryzysowa Narzeczona']], 'Lady Pank')
    assert not judge_truth([['Metallica', 'Nothing else matters'], ['Sunga Jung', 'Nothing else matters']], 'Adele')


def test_check(capsys):
    check('Three Days Grace : Animal I have become')
    out, err = capsys.readouterr()
    assert out == 'Three Days Grace sings Animal I have become\n'
    try:
        check('Metallica : Animal I have become')
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert out == 'Metallica probably doesn\'t sing Animal I have become\n'
