
from doc_test import add 

def test_can_add_num():
    assert add(8,4) == 12

def test_can_add_negative_num():
    assert add(-2,-4) == -6

def test_add_negative_assert():
    assert add(9,3) != 10

def test_can_concat_strings():
    assert add('hi','there') ==  'hithere'