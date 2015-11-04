# encoding=utf8

""" The elasticsearch dslquery

    Author: lipixun
    Created Time : Wed 21 Oct 2015 07:29:55 PM CST

    File Name: dslquery.py
    Description:

"""

SCORE_MODE_MUL      = 'multiply'
SCORE_MODE_REP      = 'replace'
SCORE_MODE_MIN      = 'min'
SCORE_MODE_MAX      = 'max'
SCORE_MODE_SUM      = 'sum'
SCORE_MODE_AVG      = 'avg'
SCORE_MODE_NONE     = 'none'

BOOST_MODE_MUL      = 'multiply'
BOOST_MODE_SUM      = 'sum'
BOOST_MODE_AVG      = 'avg'
BOOST_MODE_FIRST    = 'first'
BOOST_MODE_MAX      = 'max'
BOOST_MODE_MIN      = 'min'

MATCH_OPT_AND       = 'and'
MATCH_OPT_OR        = 'or'

class DslQuery(dict):
    """The dsl query root object
    """
    def __init__(self, name, body, matchedName = None):
        """Create a new DslQuery
        """
        self.name = name
        self.body = body
        # Super
        super(DslQuery, self).__init__(**{ name: body })
        # Matched name
        if matchedName:
            self.matchedName = matchedName

    def getTopLevelDefinition(self):
        """Get the top level definition for the query
        """
        return self.body

    @property
    def matchedName(self):
        """Get the matched name for this query
        """
        return self.getTopLevelDefinition().get('_name')

    @matchedName.setter
    def matchedName(self, value):
        """Set the matched name for this query
        """
        self.getTopLevelDefinition()['_name'] = value

    @matchedName.deleter
    def matchedName(self):
        """Delete the matched name for this query
        """
        definition = self.getTopLevelDefinition()
        if '_name' in definition:
            del definition['_name']

class MatchAll(DslQuery):
    """Match all query
    """
    def __init__(self, boost = None, matchedName = None):
        """Create a new MatchAll object
        """
        body = {}
        if not boost is None:
            body['boost'] = boost
        super(MatchAll, self).__init__('match_all', body, matchedName)

class MatchQuery(DslQuery):
    """The match query
    """
    def __init__(self, field, query, type = None, operator = None, slop = None, matchedName = None):
        """Create a new MatchQuery
        """
        body = { 'query': query }
        if type:
            body['type'] = type
        if operator:
            body['operator'] = operator
        if not slop is None:
            body['slop'] = slop
        body = { field: body }
        # Super
        super(MatchQuery, self).__init__('match', body, matchedName)

    def getTopLevelDefinition(self):
        """Get the top level definition for the query
        """
        return self.body.values()[0]

class TermQuery(DslQuery):
    """The term query
    """
    def __init__(self, field, value, boost = None, matchedName = None):
        """Create a new TermQuery
        """
        body = { 'value': value }
        if not boost is None:
            body['boost'] = boost
        body = { field: body }
        # Super
        super(TermQuery, self).__init__('term', body, matchedName)

    def getTopLevelDefinition(self):
        """Get the top level definition for the query
        """
        return self.body.values()[0]

class TermsQuery(DslQuery):
    """The terms query
    """
    def __init__(self, field, values, boost = None, matchedName = None):
        """Create a new TermsQuery
        """
        body = { 'value': values }
        if not boost is None:
            body['boost'] = boost
        body = { field: body }
        # Super
        super(TermsQuery, self).__init__('terms', body, matchedName)

    def getTopLevelDefinition(self):
        """Get the top level definition for the query
        """
        return self.body.values()[0]

class RangeQuery(DslQuery):
    """The range query
    """
    def __init__(self, field, gt = None, gte = None, lt = None, lte = None, boost = None, matchedName = None):
        """Create a new RangeQuery
        """
        body = {}
        if not gt is None:
            body['gt'] = gt
        if not gte is None:
            body['gte'] = gte
        if not lt is None:
            body['lt'] = lt
        if not lte is None:
            body['lte'] = lte
        if not boost is None:
            body['boost'] = boost
        body = { field: body }
        # Super
        super(RangeQuery, self).__init__('range', body, matchedName)

    def getTopLevelDefinition(self):
        """Get the top level definition for the query
        """
        return self.body#.values()[0]

class ExistsQuery(DslQuery):
    """The exists query
    """
    def __init__(self, field, matchedName = None):
        """Create a new ExistsQuery
        """
        super(ExistsQuery, self).__init__('exists', { 'field': field }, matchedName)

class MissingQuery(DslQuery):
    """The missing query
    """
    def __init__(self, field, matchedName = None):
        """Create a new MissingQuery
        """
        super(MissingQuery, self).__init__('missing', { 'field': field }, matchedName)

class RegexpQuery(DslQuery):
    """The regexp query
    """
    def __init__(self, field, value, boost = None, flags = None, maxDeterminizedStates = None, matchedName = None):
        """Create a new RegexpQuery
        """
        body = { 'value': value }
        if not boost is None:
            body['boost'] = boost
        if not flags is None:
            body['flags'] = flags
        if not maxDeterminizedStates is None:
            body['max_determinized_states'] = maxDeterminizedStates
        body = { field: body }
        # Super
        super(RegexpQuery, self).__init__('regexp', body, matchedName)

    def getTopLevelDefinition(self):
        """Get the top level definition for the query
        """
        return self.body.values()[0]

class IdsQuery(DslQuery):
    """The ids query
    """
    def __init__(self, values, type = None, matchedName = None):
        """Create a new IdsQuery
        """
        body = { 'values': values }
        if not type is None:
            body['type'] = type
        # Super
        super(IdsQuery, self).__init__('ids', body, matchedName)

class ConstantScoreQuery(DslQuery):
    """The constant score query
    """
    def __init__(self, filter, boost = None, matchedName = None):
        """Create a new ConstantScoreQuery
        """
        body = { 'filter': filter }
        if not boost is None:
            body['boost'] = boost
        # Super
        super(ConstantScoreQuery, self).__init__('constant_score', body, matchedName)

class BoolQuery(DslQuery):
    """The bool query
    """
    def __init__(self, must = None, filter = None, should = None, mustNot = None, boost = None, minimumShouldMatch = None, matchedName = None):
        """Create a new BoolQuery
        """
        body = {}
        if not must is None:
            body['must'] = must
        if not filter is None:
            body['filter'] = filter
        if not should is None:
            body['should'] = should
        if not mustNot is None:
            body['must_not'] = mustNot
        if not boost is None:
            body['boost'] = boost
        if not minimumShouldMatch is None:
            body['minimum_should_match'] = minimumShouldMatch
        # Done
        super(BoolQuery, self).__init__('bool', body, matchedName)

class FunctionScoreQuery(DslQuery):
    """The function score query
    """
    def __init__(self, query, functions, maxBoost = None, scoreMode = None, boostMode = None, minScore = None, boost = None, matchedName = None):
        """Create a new FunctionScoreQuery
        """
        body = { 'query': query, 'functions': functions }
        if not maxBoost is None:
            body['max_boost'] = maxBoost
        if not scoreMode is None:
            body['score_mode'] = scoreMode
        if not boostMode is None:
            body['boost_mode'] = boostMode
        if not minScore is None:
            body['min_score'] = minScore
        if not boost is None:
            body['boost'] = boost
        # Super
        super(FunctionScoreQuery, self).__init__('function_score', body, matchedName)

class Function(dict):
    """The function score function
    """
    def __init__(self, name, body, filter = None, weight = None):
        """Create a new Function
        """
        self.name = name
        self.body = body
        # Set params
        if not name is None:
            params = { name: body }
        else:
            params = {}
        if filter:
            params['filter'] = filter
        if not weight is None:
            params['weight'] = weight
        # Super
        super(Function, self).__init__(**params)

    @property
    def filter(self):
        """Get the filter
        """
        return self.get('filter')

    @filter.setter
    def filter(self, value):
        """Set the filter
        """
        self['filter'] = value

    @property
    def weight(self):
        """Get the weight
        """
        return self.get('weight')

    @weight.setter
    def weight(self, value):
        """Set the weight
        """
        self['weight'] = value

class EmptyFunction(Function):
    """The empty function
    """
    def __init__(self, filter = None, weight = None):
        """Create a new EmptyFunction
        """
        super(EmptyFunction, self).__init__(None, None, filter, weight)

class ScriptScoreFunction(Function):
    """The script score function
    """
    def __init__(self, script, filter = None, weight = None):
        """Create a new ScriptScoreFunction
        """
        super(ScriptScoreFunction, self).__init__('script_score', { 'script': script }, filter, weight)

class RandomFunction(Function):
    """The random function
    """
    def __init__(self, seed = None, filter = None, weight = None):
        """Create a new RandomFunction
        """
        super(RandomFunction, self).__init__('random_score', { 'seed': seed } if not seed is None else {}, filter, weight)

class NestedQuery(DslQuery):
    """The nested query
    """
    def __init__(self, path, query, scoreMode = None, innerHits = None, matchedName = None):
        """Create a new NestedQuery
        """
        body = { 'path': path, 'query': query }
        if not scoreMode is None:
            body['score_mode'] = scoreMode
        if not innerHits is None:
            body['inner_hits'] = innerHits
        # Super
        super(NestedQuery, self).__init__('nested', body, matchedName)

    @property
    def innerHits(self):
        """Get the inner hits
        """
        return self.body.get('inner_hits')

    @innerHits.setter
    def innerHits(self, value):
        """Set the inner hits
        """
        self.body['inner_hits'] = value

class HasChildQuery(DslQuery):
    """The has child query 
    """
    def __init__(self, type, query, scoreMode = None, minChildren = None, maxChildren = None, innerHits = None, matchedName = None):
        """Create a new HasChildQuery
        """
        body = { 'type': type, 'query': query }
        if not scoreMode is None:
            body['score_mode'] = scoreMode
        if not minChildren is None:
            body['min_children'] = minChildren
        if not maxChildren is None:
            body['max_children'] = maxChildren
        if not innerHits is None:
            body['inner_hits'] = innerHits
        # Super
        super(HasChildQuery, self).__init__('has_child', body, matchedName)
    
    @property
    def innerHits(self):
        """Get the inner hits
        """
        return self.body.get('inner_hits')

    @innerHits.setter
    def innerHits(self, value):
        """Set the inner hits
        """
        self.body['inner_hits'] = value

class HasParentQuery(DslQuery):
    """The has parent query 
    """
    def __init__(self, type, query, scoreMode = None, innerHits = None, matchedName = None):
        """Create a new HasParentQuery
        """
        body = { 'type': type, 'query': query }
        if not scoreMode is None:
            body['score_mode'] = scoreMode
        if not innerHits is None:
            body['inner_hits'] = innerHits
        # Super
        super(HasParentQuery, self).__init__('has_parent', body, matchedName)
    
    @property
    def innerHits(self):
        """Get the inner hits
        """
        return self.body.get('inner_hits')

    @innerHits.setter
    def innerHits(self, value):
        """Set the inner hits
        """
        self.body['inner_hits'] = value

