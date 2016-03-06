## encoding=utf8

""" The dsl query test
    Author: lipixun
    Created Time : Fri 23 Oct 2015 03:19:59 PM CST

    File Name: dslquery.py
    Description:

"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from os.path import abspath, dirname, join

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from elastic.search.dslquery import *

def test_MatchAll():
    """Test MatchAll query
    """
    assert MatchAll(10) == { 'match_all': { 'boost': 10 } }

def test_MatchQuery():
    """Test the match query
    """
    assert MatchQuery('afield', 'aquery') == { 'match': { 'afield': { 'query': 'aquery' } } }
    assert MatchQuery('afield', 'aquery', 'phrase', 10) == {
            'match': {
                'afield': {
                    'query': 'aquery',
                    'type': 'phrase',
                    'slop': 10
                    }
                }
            }

def test_TermQuery():
    """Test the term query
    """
    assert TermQuery('afield', 'aquery', 10) == { 'term': { 'afield': { 'value': 'aquery', 'boost': 10 } } }

def test_TermsQuery():
    """Test the terms query
    """
    assert TermsQuery('afield', [ 'avalue1', 'avalue2' ], 10) == {
            'terms': {
                'afield': {
                    'value': [ 'avalue1', 'avalue2' ],
                    'boost': 10
                    }
                }
            }

def test_RangeQuery():
    """Test the range query
    """
    assert RangeQuery('afield', 'gtv', 'gtev', 'ltv', 'ltev', 10) == {
            'range': {
                'afield': {
                    'gt': 'gtv',
                    'gte': 'gtev',
                    'lt': 'ltv',
                    'lte': 'ltev',
                    'boost': 10
                    }
                }
            }

def test_ExistsQuery():
    """Test the exists query
    """
    assert ExistsQuery('afield') == {
            'exists': {
                'field': 'afield'
                }
            }

def test_MissingQuery():
    """Test the missing query
    """
    assert MissingQuery('afield') == {
            'missing': {
                'field': 'afield'
                }
            }

def test_RegexpQuery():
    """Test the regexp query
    """
    assert RegexpQuery('afield', 'avalue', 10) == {
            'regexp': {
                'afield': {
                    'value': 'avalue',
                    'boost': 10
                    }
                }
            }

def test_IdsQuery():
    """Test ids query
    """
    assert IdsQuery([ '1', '2' ]) == { 'ids': { 'values': [ '1', '2' ] } }

def test_ConstantScoreQuery():
    """Test constant score query
    """
    assert ConstantScoreQuery(TermQuery('afield', 'avalue'), 10) == {
            'constant_score': {
                'filter': {
                    'term': {
                        'afield': {
                            'value': 'avalue'
                            }
                        }
                    },
                'boost': 10
                }
            }

def test_BoolQuery():
    """Test bool query
    """
    assert BoolQuery(
            TermQuery('mustField', 'mustValue'),
            TermQuery('filterField', 'filterValue'),
            [
                TermQuery('shouldField1', 'shouldValue1'),
                TermQuery('shouldField2', 'shouldValue2')
            ],
            TermQuery('mustNotField', 'mustNotValue'),
            10,
            100) == {
                    'bool': {
                        'must': {
                            'term': {
                                'mustField': {
                                    'value': 'mustValue'
                                    }
                                }
                            },
                        'filter': {
                            'term': {
                                'filterField': {
                                    'value': 'filterValue'
                                    }
                                }
                            },
                        'should': [
                            {
                                'term': {
                                    'shouldField1': {
                                        'value': 'shouldValue1'
                                        }
                                    }
                                },
                            {
                                'term': {
                                    'shouldField2': {
                                        'value': 'shouldValue2'
                                        }
                                    }
                                }
                            ],
                        'must_not': {
                            'term': {
                                'mustNotField': {
                                    'value': 'mustNotValue'
                                    }
                                }
                            },
                        'boost': 10,
                        'minimum_should_match': 100
                        }
                    }

def test_FunctionScoreQuery():
    """Test the function score query
    """
    assert FunctionScoreQuery(
            TermQuery('afield', 'avalue'),
            [
                EmptyFunction(TermQuery('afield1', 'avalue1'), 1),
                ScriptScoreFunction('_score * 10', TermQuery('afield2', 'avalue2'), 2),
                RandomFunction(100, TermQuery('afield3', 'avalue3'), 3)
            ],
            10,
            SCORE_MODE_SUM,
            BOOST_MODE_MAX,
            100,
            1000
            ) == {
                    'function_score': {
                        'query': {
                            'term': {
                                'afield': {
                                    'value': 'avalue'
                                    }
                                }
                            },
                        'functions': [
                            {
                                'filter': {
                                    'term': {
                                        'afield1': {
                                            'value': 'avalue1'
                                            }
                                        }
                                    },
                                'weight': 1
                            },
                            {
                                'filter': {
                                    'term': {
                                        'afield2': {
                                            'value': 'avalue2'
                                            }
                                        }
                                    },
                                'weight': 2,
                                'script_score': {
                                    'script': '_score * 10'
                                    }
                            },
                            {
                                'filter': {
                                    'term': {
                                        'afield3': {
                                            'value': 'avalue3'
                                            }
                                        }
                                    },
                                'weight': 3,
                                'random_score': {
                                    'seed': 100
                                    }
                            }
                        ],
                        'max_boost': 10,
                        'score_mode': 'sum',
                        'boost_mode': 'max',
                        'min_score': 100,
                        'boost': 1000
                    }
                }

def test_NestedQuery():
    """Test the nested query
    """
    assert NestedQuery('nestedPath', TermQuery('afield', 'avalue'), SCORE_MODE_MAX, {}) == {
            'nested': {
                'path': 'nestedPath',
                'query': {
                    'term': {
                        'afield': {
                            'value': 'avalue'
                            }
                        }
                    },
                'score_mode': 'max',
                'inner_hits': {}
                }
            }

def test_HasChildQuery():
    """Test the has child query
    """
    assert HasChildQuery('childType', TermQuery('afield', 'avalue'), SCORE_MODE_MAX, 10, 100, {}) == {
            'has_child': {
                'type': 'childType',
                'query': {
                    'term': {
                        'afield': {
                            'value': 'avalue'
                            }
                        }
                    },
                'score_mode': 'max',
                'min_children': 10,
                'max_children': 100,
                'inner_hits': {}
                }
            }

def test_HasParentQuery():
    """Test the has parent query
    """
    assert HasParentQuery('parentType', TermQuery('afield', 'avalue'), SCORE_MODE_MAX, {}) == {
            'has_parent': {
                'type': 'parentType',
                'query': {
                    'term': {
                        'afield': {
                            'value': 'avalue'
                            }
                        }
                    },
                'score_mode': 'max',
                'inner_hits': {}
                }
            }

