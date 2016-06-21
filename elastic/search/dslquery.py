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
BOOST_MODE_REP      = 'replace'
BOOST_MODE_SUM      = 'sum'
BOOST_MODE_AVG      = 'avg'
BOOST_MODE_FIRST    = 'first'
BOOST_MODE_MAX      = 'max'
BOOST_MODE_MIN      = 'min'

MATCH_OPT_AND       = 'and'
MATCH_OPT_OR        = 'or'

MULTI_MATCH_TYPE_BEST_FIELDS        = 'best_fields'
MULTI_MATCH_TYPE_MOST_FIELDS        = 'most_fields'
MULTI_MATCH_TYPE_CROSS_FIELDS       = 'cross_fields'
MULTI_MATCH_TYPE_PHRASE             = 'phrase'
MULTI_MATCH_TYPE_PHRASE_PREFIX      = 'phrase_prefix'

DECAY_FUNCTION_GAUSS    = 'gauss'
DECAY_FUNCTION_EXP      = 'exp'
DECAY_FUNCTION_LINEAR   = 'linear'

DECAY_FUNCTION_MULTI_VALUE_MODE_MIN         = 'min'
DECAY_FUNCTION_MULTI_VALUE_MODE_MAX         = 'max'
DECAY_FUNCTION_MULTI_VALUE_MODE_AVG         = 'avg'
DECAY_FUNCTION_MULTI_VALUE_MODE_SUM         = 'sum'

class DslQuery(dict):
    """The dsl query root object
    """
    def __init__(self, name, body, boost = None, matchedName = None):
        """Create a new DslQuery
        """
        self.name = name
        self.body = body
        # Super
        super(DslQuery, self).__init__(**{ name: body })
        # Boost
        if not boost is None:
            self.boost = boost
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
        self.getTopLevelDefinition().pop('_name', None)

    @property
    def boost(self):
        """Get the boost for this query
        """
        return self.getTopLevelDefinition().get('boost')

    @boost.setter
    def boost(self, value):
        """Set the boost for this query
        """
        self.getTopLevelDefinition()['boost'] = value

    @boost.deleter
    def boost(self):
        """Delete the boost for this query
        """
        self.getTopLevelDefinition().pop('boost', None)

class MatchAllQuery(DslQuery):
    """Match all query
    """
    def __init__(self, boost = None, matchedName = None):
        """Create a new MatchAll object
        """
        super(MatchAllQuery, self).__init__('match_all', {}, boost, matchedName)

class MatchQuery(DslQuery):
    """The match query
    Document: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html
    """
    def __init__(self,
        field,
        query,
        slop = None,
        type = None,
        operator = None,
        fuzziness = None,
        maxExpansions = None,
        minimumShouldMatch = None,
        boost = None,
        matchedName = None
        ):
        """Create a new MatchQuery
        """
        body = { 'query': query }
        if type:
            body['type'] = type
        if operator:
            body['operator'] = operator
        if not minimumShouldMatch is None:
            body['minimum_should_match'] = minimumShouldMatch
        if not fuzziness is None:
            body['fuzziness'] = fuzziness
        if not maxExpansions is None:
            body['max_expansions'] = maxExpansions
        if not slop is None:
            body['slop'] = slop
        body = { field: body }
        # Super
        super(MatchQuery, self).__init__('match', body, boost, matchedName)

    def getTopLevelDefinition(self):
        """Get the top level definition for the query
        """
        return self.body.values()[0]

class MultiMatchQuery(DslQuery):
    """The multi match query
    """
    def __init__(self, fields, query, type = None, operator = None, tieBreaker = None, minimumShouldMatch = None, boost = None, matchedName = None):
        """Create a new MultiMatchQuery
        """
        body = {
            'fields': fields,
            'query': query
        }
        if type:
            body['type'] = type
        if operator:
            body['operator'] = operator
        if not tieBreaker is None:
            body['tie_breaker'] = tieBreaker
        if not minimumShouldMatch is None:
            body['minimum_should_match'] = minimumShouldMatch
        # Super
        super(MultiMatchQuery, self).__init__('multi_match', body, boost, matchedName)

class TermQuery(DslQuery):
    """The term query
    """
    def __init__(self, field, value, boost = None, matchedName = None):
        """Create a new TermQuery
        """
        # Super
        super(TermQuery, self).__init__('term', { field: { 'value': value } }, boost, matchedName)

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
        # Super
        super(TermsQuery, self).__init__('terms', { field: values }, boost, matchedName)

    def getTopLevelDefinition(self):
        """Get the top level definition for the query
        """
        return self.body

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
        body = { field: body }
        # Super
        super(RangeQuery, self).__init__('range', body, boost, matchedName)

    def getTopLevelDefinition(self):
        """Get the top level definition for the query
        """
        return self.body#.values()[0]

class ExistsQuery(DslQuery):
    """The exists query
    """
    def __init__(self, field, boost = None, matchedName = None):
        """Create a new ExistsQuery
        """
        super(ExistsQuery, self).__init__('exists', { 'field': field }, boost, matchedName)

class MissingQuery(DslQuery):
    """The missing query
    """
    def __init__(self, field, boost = None, matchedName = None):
        """Create a new MissingQuery
        """
        super(MissingQuery, self).__init__('missing', { 'field': field }, boost, matchedName)

class RegexpQuery(DslQuery):
    """The regexp query
    """
    def __init__(self, field, value, flags = None, maxDeterminizedStates = None, boost = None, matchedName = None):
        """Create a new RegexpQuery
        """
        body = { 'value': value }
        if not flags is None:
            body['flags'] = flags
        if not maxDeterminizedStates is None:
            body['max_determinized_states'] = maxDeterminizedStates
        body = { field: body }
        # Super
        super(RegexpQuery, self).__init__('regexp', body, boost, matchedName)

    def getTopLevelDefinition(self):
        """Get the top level definition for the query
        """
        return self.body.values()[0]

class IdsQuery(DslQuery):
    """The ids query
    """
    def __init__(self, values, type = None, boost = None, matchedName = None):
        """Create a new IdsQuery
        """
        body = { 'values': values }
        if not type is None:
            body['type'] = type
        # Super
        super(IdsQuery, self).__init__('ids', body, boost, matchedName)

class ConstantScoreQuery(DslQuery):
    """The constant score query
    """
    def __init__(self, filter, boost = None, matchedName = None):
        """Create a new ConstantScoreQuery
        """
        # Super
        super(ConstantScoreQuery, self).__init__('constant_score', { 'filter': filter }, boost, matchedName)

class BoolQuery(DslQuery):
    """The bool query
    """
    def __init__(self, must = None, filter = None, should = None, mustNot = None, minimumShouldMatch = None, boost = None, matchedName = None):
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
        if not minimumShouldMatch is None:
            body['minimum_should_match'] = minimumShouldMatch
        # Done
        super(BoolQuery, self).__init__('bool', body, boost, matchedName)

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
        # Super
        super(FunctionScoreQuery, self).__init__('function_score', body, boost, matchedName)

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

class DecayFunction(Function):
    """The decay function
    """
    def __init__(self, decayFunctionName, field, origin = None, scale = None, offset = None, decay = None, multiValueMode = None, filter = None, weight = None):
        """Create a new DecayFunction
        """
        body = {}
        if not origin is None:
            body['origin'] = origin
        if not scale is None:
            body['scale'] = scale
        if not offset is None:
            body['offset'] = offset
        if not decay is None:
            body['decay'] = decay
        if not multiValueMode is None:
            body['multi_value_mode'] = multiValueMode
        # Super
        super(DecayFunction, self).__init__(decayFunctionName, { field: body }, filter, weight)

class NestedQuery(DslQuery):
    """The nested query
    """
    def __init__(self, path, query, scoreMode = None, innerHits = None, boost = None, matchedName = None):
        """Create a new NestedQuery
        """
        body = { 'path': path, 'query': query }
        if not scoreMode is None:
            body['score_mode'] = scoreMode
        if not innerHits is None:
            body['inner_hits'] = innerHits
        # Super
        super(NestedQuery, self).__init__('nested', body, boost, matchedName)

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
    def __init__(self, type, query, scoreMode = None, minChildren = None, maxChildren = None, innerHits = None, boost = None, matchedName = None):
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
        super(HasChildQuery, self).__init__('has_child', body, boost, matchedName)

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
    def __init__(self, type, query, scoreMode = None, innerHits = None, boost = None, matchedName = None):
        """Create a new HasParentQuery
        """
        body = { 'type': type, 'query': query }
        if not scoreMode is None:
            body['score_mode'] = scoreMode
        if not innerHits is None:
            body['inner_hits'] = innerHits
        # Super
        super(HasParentQuery, self).__init__('has_parent', body, boost, matchedName)

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

class InnerHits(dict):
    """The inner hits
    """
    def __init__(self, name = None, source = None, fields = None, highlights = None, sort = None, _from = 0, size = 1):
        """Create a new InnerHits
        """
        body = {}
        if name:
            body['name'] = name
        if not source is None:
            body['_source'] = source
        if fields:
            body['fielddata_fields'] = fields
        if highlights:
            body['highlight'] = { 'fields': highlights }
        if sort:
            body['sort'] = sort
        if not _from is None:
            body['from'] = _from
        if not size is None:
            body['size'] = size
        # Super
        super(InnerHits, self).__init__(**body)
