
import os
import scraping_class

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


