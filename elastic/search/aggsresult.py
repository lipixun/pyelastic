#!/usr/bin/env python
#coding=utf8
"""
# Author: f
# Created Time : 一  9/19 16:52:47 2016

# File Name: /Users/f/code/datamiller/pyelastic/elastic/search/aggresult.py
# Description:

"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class AggsResult(dict):
    """The elastcicsearch aggregation result"""
    def __init__(self, body, name = None):
        self._name = name
        super(AggsResult, self).__init__(body)

    @property
    def hasBucket(self):
        return isinstance(self, BucketAggsResult)

    def child(self, name):
        if name not in self:
            return None
        if 'buckets' in self[name]:
            return BucketAggsResult(self[name], name)
        else:
            return AggsResult(self[name], name)

    @property
    def name(self):
        return self._name
    
    @property
    def value(self):
        if 'value' in self:
            return self['value']
        elif 'doc_count' in self:
            return self['doc_count']
        else:
            return None

class Bucket(AggsResult):
    """
        Aggregation result bucket
    """
    @property
    def key(self):
        return self['key']

    @property
    def key_as_string(self):
        return self.get('key_as_string')

    @property
    def name(self):
        return self.get('key_as_string') or self.get('key')

class BucketAggsResult(AggsResult):
    """
        Bucket aggregation result
    """
    @property
    def buckets(self):
        for bucket in self['buckets']:
            yield Bucket(bucket)

    @property
    def otherCount(self):
        return self.get('sum_other_doc_count', 0)

    @property
    def total(self):
        bucket_count = sum([bucket.value for bucket in self.buckets])
        return bucket_count + self.otherCount
