# encoding=utf8

""" The search result
    Author: lipixun
    Created Time : Wed 04 Nov 2015 12:48:31 PM CST

    File Name: result.py
    Description:

"""

class Result(dict):
    """The elasticsearch result
    """
    @property
    def total(self):
        """Get the total result number
        """
        return self['hits']['total']

    @property
    def maxScore(self):
        """Get the max score
        """
        return self['hits']['max_score']

    @property
    def isTimedOut(self):
        """Get if the search is timed out
        """
        return self['timed_out']

    @property
    def hits(self):
        """Get the hitted items
        """
        hits = self['hits']['hits']
        if hits:
            # Check if the hit item is created
            if not isinstance(hits[0], HitItem):
                hits = [ HitItem(js) for js in hits ]
                self['hits']['hits'] = hits
                return hits
            else:
                return hits
        else:
            return tuple()

    @property
    def aggs(self):
        """Get the aggregation results
        """
        return self.get('aggregations')

class HitItem(dict):
    """The hitted item
    """
    @property
    def id(self):
        """Get the id
        """
        return self['_id']

    @property
    def type(self):
        """Get the type
        """
        return self['_type']

    @property
    def index(self):
        """Get the index
        """
        return self['_index']

    @property
    def score(self):
        """Get the score
        """
        return self['_score']

    @property
    def source(self):
        """Get the source
        """
        return self.get('_source')

    @property
    def fields(self):
        """Get the fields
        """
        return self.get('fields')

    @property
    def highlights(self):
        """Get the highlights
        """
        return self.get('highlight')

    @property
    def matchedQueries(self):
        """Get the matched queries
        """
        return self.get('matched_queries')

    @property
    def innerHits(self):
        """Get the inner hits
        """
        innerHits = self.get('inner_hits')
        if innerHits:
            if not isinstance(innerHits.values()[0], Result):
                innerHits = dict(map(lambda (k, v): (k, Result(v)), innerHits.iteritems()))
                self['inner_hits'] = innerHits
                return innerHits
            else:
                return innerHits
