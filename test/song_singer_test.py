from song_singer.ConnectionException import *
from song_singer.main import *
import pytest

def parse_inquiry_test():
  assert parse_inquiry('Leonard Cohen : Hallelujah') == ['Leonard Cohen','Hallelujah']
  assert parse_inquiry('Leonard Cohen Hallelujah') == None
  assert parse_inquiry('') == None
  
def safe_get_test():
  with pytest.raises(ConnectionException):
    safe_get('https://github.com/AGHPythonCourse2017/zad3-chudy7991')
  safe_get('https://github.com/AGHPythonCourse2017/zad3-chudy1997/edit/master/test/song_singer_test.py')!=None
  
def get_titles_from_addr_test():
  pass

def remove_wrong_titles_test():
  pass

def judge_truth_test():
  pass

def unicode_test():
  pass

def check_test():
  pass
