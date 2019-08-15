
import os
import scraping_class

def _report(s):
    print(
    """--------------------------------
    {}
    """.format(s)
    )

def testConnectorInit():
    t = scraping_class.Connector('testfile.log')
    assert str(t.log) == 'Logfile testfile.log'
    _report('Passes testConnectorInit')

def testConnectorInitOverwrite():
    t = scraping_class.Connector('testfile.log')

    with open('testfile.log', 'w') as f:
        f.write('something random')

    t = scraping_class.Connector('testfile.log', overwrite_log = True)

    with open('testfile.log', 'r') as f:
        assert f.read() != 'something random'

    _report('Passes testConnectorInitOverwrite')


def _testConnectorGetOverWrite():
    t = scraping_class.Connector('testfile2.log', overwrite_log= True)
    t.get('https://www.google.com', 'PNAME')

    with open('testfile2.log', 'r') as f:
        assert len(f.read().split('\n')) == 2

    t.get('https://www.google.com', 'PNAME')
    t.get('https://www.google.com', 'PNAME')

    with open('testfile2.log', 'r') as f:
        assert len(f.read().split('\n')) == 4


def testConnectorGetOverwrite():
    # Do this twice to be sure that the overwrite 
    # happens between initializations of the class
    # only.
    _testConnectorGetOverWrite()
    _testConnectorGetOverWrite()
    _report('Passes testConnectorGetOverwrite')


def cleanup():
    files = 'test.log', 'testfile.log', 'testfile2.log'
    for f in files:
        try:
            os.remove(f)
        except:
            pass

    
if __name__ == '__main__':
    testConnectorInit()
    testConnectorInitOverwrite()
    testConnectorGetOverwrite()
    cleanup()