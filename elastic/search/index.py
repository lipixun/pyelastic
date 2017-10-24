# encoding=utf8

""" The elasticsearch index
    Author: lipixun
    Created Time : Sun 25 Oct 2015 08:01:48 PM CST

    File Name: index.py
    Description:

"""

from sets import Set
from collections import namedtuple

from dslquery import HasChildQuery, HasParentQuery

SCORE_MODE_NONE = 'none'
SCORE_MODE_SUM = 'sum'
SCORE_MODE_MAX = 'max'
SCORE_MODE_TOTAL = 'total'
SCORE_MODE_AVG = 'avg'

class Index(object):
    """The index
    """
    def __init__(self, name, doc = None):
        """Create a new Index
        """
        self.name = name
        self.docs = {}
        self.getAllDocument(doc, self.docs)

    def __str__(self):
        """Convert to string
        """
        return 'Index [%s] Docs [%s]' % (self.name, ','.join(self.docs.iterkeys()) if self.docs else '')

    def __getitem__(self, doc):
        """Get document
        """
        return self.docs.get(doc)

    def getRelation(self, fromDoc, toDoc):
        """Get the relation between doc
        """
        document = self[fromDoc]
        if not document:
            return
        return document.correlate(toDoc)

    def getAllDocument(self, doc, allDict):
        """ Get all the related documents
        """
        if not doc:
            return
        if doc.name:
            allDict[doc.name] = doc
        if doc.children:
            for key, child in doc.children.items():
                self.getAllDocument(child, allDict)

class Document(object):
    """The document
    """
    def __init__(self, name, parent = None, children = None):
        """Create a new Document
        """
        self.name = name
        self.parent = parent
        self.children = children or {}      # Key is name, value is Document object

    def __str__(self):
        """Convert to string
        """
        return 'Document [%s] parent [%s] children [%s]' % (self.name, self.parent or '', ','.join(self.children.iterkeys()) if self.children else '')

    def correlate(self, name):
        """Get the corelation to another document
        Parameters:
            name                        The document name
        Returns:
            DocCorrelation object if correlation found else will be None (If the name is the document itself, then None will be returned)
        """
        if name == self.name:
            return
        visitedDocs = Set([ self.name ])
        visitingQueue = [ (self, []) ]
        while visitingQueue:
            doc, relations = visitingQueue.pop(0)
            if doc.name == name:
                #relations example: [("child","es_emr")]
                return DocCorrelation.fromRelations(relations)
            if doc.parent and not doc.parent.name in visitedDocs:
                newRelations = list(relations)
                newRelations.append(('parent', doc.parent.name))
                visitingQueue.append((doc.parent, newRelations))
                visitedDocs.add(doc.parent.name)
            if doc.children:
                for childDoc in doc.children.itervalues():
                    if not childDoc.name in visitedDocs:
                        newRelations = list(relations)
                        newRelations.append(('child', childDoc.name))
                        visitingQueue.append((childDoc, newRelations))
                        visitedDocs.add(childDoc.name)
        # Nothing found

PathNode = namedtuple('PathNode', 'type,name')

class DocCorrelation(object):
    """The document correlation
    """
    def __init__(self, path):
        """Create a new Correlation
        """
        self.path = path

    def __len__(self):
        """Get the length of this relation
        """
        return len(self.path)

    def reverse(self):
        """Get the reverse one
        """
        return DocCorrelation(list(reversed(self.path)))

    def getQuery(self, query, scoreMode = None, minChildren = None, maxChildren = None, innerHits = None, namedFunc = None):
        """Get the query from current document correlation
        More explanation:
            Suppose the path is from document A to document B, when we get query according to this correlation, that means:
            We are currently searching the document A and have a query must be matched in B
        Parameters:
            query                       The query to wrap
            scoreMode                   The score mode
            minChildren                 The min children number
            maxChildren                 The max children number
            innerHits                   The inner hits config
            namedFunc                   A function to name the generated query, the function has one parameter - The generated query, returns the name
        Returns:
            The DslQuery (The HasParentQuery or HasChildQuery)
        """
        for node in reversed(self.path):
            if node.type == 'parent':
                query = HasParentQuery(node.name, query, scoreMode, innerHits)
            else:
                query = HasChildQuery(node.name, query, scoreMode, minChildren, maxChildren, innerHits)
        # Done
        return query

    @classmethod
    def fromRelations(cls, relations):
        """From relations
        """
        path = []
        for t, name in relations:
            path.append(PathNode(t, name))
        # Done
        return DocCorrelation(path)
