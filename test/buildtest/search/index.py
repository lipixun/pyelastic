# encoding=utf8

""" The index test
    Author: lipixun
    Created Time : Sun 25 Oct 2015 09:52:54 PM CST

    File Name: index.py
    Description:

"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from os.path import abspath, dirname, join

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from elastic.search.index import Index, Document 

def test_DocumentCorrelation():
    """Test the document correlation
    """
    doc1, doc2, doc3 = Document('doc1'), Document('doc2'), Document('doc3')
    doc2.parent = doc1
    doc3.parent = doc1
    doc1.children['doc2'] = doc2
    doc1.children['doc3'] = doc3
    # Get correlation
    assert doc1.correlate('doc1') is None
    assert doc1.correlate('doc4') is None
    cor1 = doc1.correlate('doc2')
    assert len(cor1.path) == 1 and cor1.getQuery(None) == {
            'has_child': {
                'type': 'doc2',
                'query': None
                }
            }
    cor2 = doc1.correlate('doc3')
    assert len(cor2.path) == 1 and cor2.getQuery(None) == {
            'has_child': {
                'type': 'doc3',
                'query': None
                }
            }
    cor3 = doc2.correlate('doc1')
    assert len(cor3.path) == 1 and cor3.getQuery(None) == {
            'has_parent': {
                'type': 'doc1',
                'query': None
                }
            }
    cor4 = doc3.correlate('doc1')
    assert len(cor4.path) == 1 and cor4.getQuery(None) == {
            'has_parent': {
                'type': 'doc1',
                'query': None
                }
            }
    cor5 = doc2.correlate('doc3')
    assert len(cor5.path) == 2 and cor5.getQuery(None) == {
            'has_parent': {
                'type': 'doc1',
                'query': {
                    'has_child': {
                        'type': 'doc3',
                        'query': None
                        }
                    }
                }
            }
    cor6 = doc3.correlate('doc2')
    assert len(cor6.path) == 2 and cor6.getQuery(None) == {
            'has_parent': {
                'type': 'doc1',
                'query': {
                    'has_child': {
                        'type': 'doc2',
                        'query': None
                        }
                    }
                }
            }

