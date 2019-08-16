
import os
import scraping_class
from scraping_class.scraping_class import construct_query

import pytest

@pytest.fixture(scope = 'session', autouse=True)
def teardown():
    os.mkdir("tests/assets")
    yield
    print("running TEARDOWN", os.getcwd())
    files = 'tests/assets/test.log', 'tests/assets/testfile.log', 'tests/assets/testfile2.log'
    for f in files:
        try:
            os.remove(f)
        except:
            pass
    os.rmdir("tests/assets")



def test_ConnectorInit():
    t = scraping_class.Connector('tests/assets/testfile.log')
    assert str(t.log) == 'Logfile tests/assets/testfile.log'


def test_ConnectorInitOverwrite():
    t = scraping_class.Connector('tests/assets/testfile.log')

    with open('tests/assets/testfile.log', 'w') as f:
        f.write('something random')

    t = scraping_class.Connector('tests/assets/testfile.log', overwrite_log = True)

    with open('tests/assets/testfile.log', 'r') as f:
        assert f.read() != 'something random'


def _ConnectorGetOverWrite():
    t = scraping_class.Connector('tests/assets/testfile2.log', overwrite_log = True)
    assert t.log.mode == 'a'

    t.get('https://www.google.com', 'PNAME1')

    assert t.log.mode == 'a'

    with open('tests/assets/testfile2.log', 'r') as f:
        assert len(f.read().split('\n')) == 2

    t.get('https://www.google.com', 'PNAME2')
    t.get('https://www.google.com', 'PNAME3')

    with open('tests/assets/testfile2.log', 'r') as f:
        assert len(f.read().split('\n')) == 4

def test_ConnectorGetOverwrite():
    # Do this twice to be sure that the overwrite 
    # happens between initializations of the class
    # only.
    _ConnectorGetOverWrite()
    _ConnectorGetOverWrite()

def test_construct_query():
    url = 'http://random.url'
    params = {'key2': 'val2', 'key3': 'val3'}
    assert construct_query(url, params) == "http://random.url?key2=val2&key3=val3"

     #Existing '?'
    url = 'http://random.url?'
    params = {'key2': 'val2'}
    assert construct_query(url, params) == "http://random.url?key2=val2"

     #Existing parameters
    url = 'http://random.url?key1=val1'
    params = {'key2': 'val2', 'key3': 'val3'}
    assert construct_query(url, params) == "http://random.url?key1=val1&key2=val2&key3=val3"

     #No additional parameters
    url = 'http://random.url?key1=val1'
    assert construct_query(url) == "http://random.url?key1=val1"
