# encoding=utf8

""" The elasticsearch request body related data definition
    Author: lipixun
    Created Time : Sat 31 Oct 2015 11:11:13 PM CST

    File Name: requestbody.py
    Description:

"""

HL_TYPE_PLAIN       = 'plain'
HL_TYPE_POSTINGS    = 'postings'
HL_TYPE_FVH         = 'fvh'

class Highlighter(dict):
    """A highlighter
    """
    def __init__(
            self,
            type = None,
            forceSource = None,
            fragmentSize = None,
            fragmentNumber = None, 
            fragmentOffset = None,
            noMatchSize = None,
            requireFieldMatch = None,
            boundaryChars = None,
            boundaryMaxScan = None,
            matchedFields = None,
            phraseLimit = None,
            query = None
            ):
        """Create a new Highlighter
        """
        # Add attrs
        attrs = {}
        if type:
            attrs['type'] = type
        if not forceSource is None:
            attrs['force_source'] = forceSource
        if not fragmentSize is None:
            attrs['fragment_size'] = fragmentSize
        if not fragmentNumber is None:
            attrs['number_of_fragments'] = fragmentNumber
        if not fragmentOffset is None:
            attrs['fragment_offset'] = fragmentOffset
        if not noMatchSize is None:
            attrs['no_match_size'] = noMatchSize
        if not requireFieldMatch is None:
            attrs['require_field_match'] = requireFieldMatch
        if boundaryChars:
            attrs['boundary_chars'] = boundaryChars
        if boundaryMaxScan:
            attrs['boundary_max_scan'] = boundaryMaxScan
        if matchedFields:
            attrs['matched_fields'] = matchedFields
        if not phraseLimit is None:
            attrs['phrase_limit'] = phraseLimit
        if query:
            attrs['highlight_query'] = query
        # Super
        super(Highlighter, self).__init__(**attrs)

