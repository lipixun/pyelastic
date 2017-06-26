# encoding=utf8

""" The aggregation query
    Author: lipixun
    Created Time : 四 12/10 16:33:11 2015

    File Name: aggsquery.py
    Description:

        The aggregation query definitions

"""

class AggQuery(dict):
    """The aggregation query
    """
    SUPPORT_SUB_AGG = True

    def __init__(self, name, body, children = None):
        """Create a new AggsQuery
        """
        self._name = name
        self._body = body
        if self.SUPPORT_SUB_AGG:
            self._children = children or {}
            # Super
            super(AggQuery, self).__init__({ self.TYPENAME: self._body, 'aggs': self._children })
        else:
            self._children = None
            if children:
                raise ValueError('Aggregation [%s] donnot support sub aggregation' % self.TYPENAME)
            # Super
            super(AggQuery, self).__init__({ self.TYPENAME: self._body })

    @property
    def name(self):
        """Get the name of this query
        """
        return self._name

    @property
    def body(self):
        """Get the body of this query
        """
        return self._body

    @property
    def children(self):
        """Get child aggregations
        """
        return self._children

    def addSubAggregation(self, aggQuery):
        """Add (a) sub aggregation(s)
        Parameters:
            aggQuery                    AggQuery or a tuple/list of AggQuery
        """
        if not self.SUPPORT_SUB_AGG:
            raise ValueError('Aggregation [%s] donnot support sub aggregation' % self.TYPENAME)
        if not isinstance(aggQuery, (tuple, list)):
            aggQuery = (aggQuery, )
        for q in aggQuery:
            if q.name in self._children:
                raise ValueError('Conflict aggregation name [%s]' % q.name)
            self._children[q.name] = q

# -*- ---------- Metrics aggregations --------- -*-

class CardinalityAgg(AggQuery):
    """CardinalityAgg"""
    TYPENAME="cardinality"
    SUPPORT_SUB_AGG = False

    def __init__(self, name, field = None, script = None, missing = None, precision_threshold = None):
        """
            @Brief __init__
            @Param name:
            @Param field: field to count
            @Param script:
            @Param missing: missing value is ignored by default
            @Param precision_threshold: default to 3000
        """
        body = {}
        if field:
            body['field'] = field
        if script:
            body['script'] = script
        if missing:
            body['missing'] = missing
        if precision_threshold is not None:
            body['precision_threshold'] = precision_threshold

        super(CardinalityAgg, self).__init__(name, body)


class AvgAgg(AggQuery):
    """The avg aggregation
    """
    TYPENAME = 'avg'
    SUPPORT_SUB_AGG = False

    def __init__(self, name, field = None, script = None, missing = None, children = None):
        """Create a new AvgAggs
        """
        body = {}
        if field:
            body['field'] = field
        if script:
            body['script'] = script
        if missing:
            body['missing'] = missing
        # Super
        super(AvgAgg, self).__init__(name, body, children)

class SumAgg(AggQuery):
    """The sum aggregation
    """
    TYPENAME = 'sum'
    SUPPORT_SUB_AGG = False

    def __init__(self, name, field = None, script = None, children = None):
        """Create a new SumAgg
        """
        body = {}
        if field:
            body['field'] = field
        if script:
            body['script'] = script
        # Super
        super(SumAgg, self).__init__(name, body, children)

# -*- --------- Bucket Aggregations --------- -*-

class ChildrenAgg(AggQuery):
    """The child aggregation
    """
    TYPENAME = 'children'

    def __init__(self, name, type, children = None):
        """Create a new ChildAgg object
        """
        super(ChildrenAgg, self).__init__(name, { 'type': type }, children)

DATEHISTOGRAMAGG_INTERVAL_YEAR      = 'year'
DATEHISTOGRAMAGG_INTERVAL_QUARTER   = 'quarter'
DATEHISTOGRAMAGG_INTERVAL_MONTH     = 'month'
DATEHISTOGRAMAGG_INTERVAL_WEEK      = 'week'
DATEHISTOGRAMAGG_INTERVAL_DAY       = 'day'
DATEHISTOGRAMAGG_INTERVAL_HOUR      = 'hour'
DATEHISTOGRAMAGG_INTERVAL_MINUTE    = 'minute'
DATEHISTOGRAMAGG_INTERVAL_SECOND    = 'second'

class DateHistogramAgg(AggQuery):
    """The date histogram aggregation
    """
    TYPENAME = 'date_histogram'

    def __init__(self, name, field, interval, format = None, children = None, minDocCount = None, extendedBounds = None, timeZone = None):
        """Create a new DateHistogramAgg object
        """
        body = { 'field': field, 'interval': interval }
        if minDocCount is not None:
            body['min_doc_count'] = minDocCount
        if extendedBounds:
            body['extended_bounds'] = extendedBounds
        if format:
            body['format'] = format
        if timeZone:
            body['time_zone'] = timeZone
        # Super
        super(DateHistogramAgg, self).__init__(name, body, children)

class DateRangeAgg(AggQuery):
    """The date range aggregation
    """
    TYPENAME = 'date_range'

    def __init__(self, name, field, format = None, ranges = None, children = None):
        """Create a new DateRange
        """
        body = { 'field': field }
        if format:
            body['format'] = format
        if ranges:
            body['ranges'] = ranges
        # Super
        super(DateRangeAgg, self).__init__(name, body, children)

class FilterAgg(AggQuery):
    """The filter aggregation
    """
    TYPENAME = 'filter'

    def __init__(self, name, query, children = None):
        """Create a new FilterAgg
        """
        super(FilterAgg, self).__init__(name, query, children)

class FiltersAgg(AggQuery):
    """The filters aggregation
    """
    TYPENAME = 'filters'

    def __init__(self, name, filters, children = None):
        """Create a new FiltersAgg
        """
        super(FiltersAgg, self).__init__(name, filters, children)

class HistogramAgg(AggQuery):
    """The histogram aggregation
    """
    TYPENAME = 'histogram'

    def __init__(self, name, field, interval, minDocCount = None, extendedBounds = None, order = None, keyed = None, missing = None, children = None):
        """Create a new HistogramAgg
        """
        body = { 'field': field, 'interval': interval }
        if not minDocCount is None:
            body['min_doc_count'] = minDocCount
        if extendedBounds:
            body['extended_bounds'] = extendedBounds
        if order:
            body['order'] = order
        if keyed:
            body['keyed'] = keyed
        if not missing is None:
            body['missing'] = missing
        # Super
        super(HistogramAgg, self).__init__(name, body, children)

class RangeAgg(AggQuery):
    """The range aggregation
    NOTE:
        The range from a to b is [a, b)
    """
    TYPENAME = 'range'

    def __init__(self, name, field, script = None, params = None, keyed = None, ranges = None, children = None):
        """Create a new RangeAgg
        """
        body = { 'field': field }
        if script:
            body['script'] = script
        if params:
            body['params'] = params
        if keyed:
            body['keyed'] = keyed
        if ranges:
            body['ranges'] = ranges
        # Super
        super(RangeAgg, self).__init__(name, body, children)

TERMSAGG_ORDER_ACSENDING = 'asc'
TERMSAGG_ORDER_DESCENDING = 'desc'

TERMSAGG_COLLECTMODE_DEPTH_FIRST = 'depth_first'
TERMSAGG_COLLECTMODE_BREADTH_FIRST = 'breadth_first'

class TermsAgg(AggQuery):
    """The terms aggregation
    """
    TYPENAME = 'terms'

    def __init__(self, name, field, size = None, minDocCount = None, order = None, include = None, exclude = None, collectMode = None, children = None):
        """Create a new TermsAgg
        """
        body = { 'field': field }
        if not size is None:
            body['size'] = size
        if not minDocCount is None:
            body['min_doc_count'] = minDocCount
        if order:
            body['order'] = order
        if include:
            body['include'] = include
        if exclude:
            body['exclude'] = exclude
        if collectMode:
            body['collect_mode'] = collectMode
        # Super
        super(TermsAgg, self).__init__(name, body, children)

