# Helper functions
import re

def decompose_querystring(response=None, querystring=None):
    """
    Decompose the querystring back into keywords known in the facets 
    Only full phrases are considered (hence the \s (any whitespace, trumps \b in this case)

    Keyword Arguments: 
    response - the elasticsearch-dsl response object
    querystring - the querystring from the URL """
    qdict = {'lower': [],
             'normal': []}
    if response and querystring:
        for term in response.facets:
            for item, _, _ in response.facets[term]:
                pat = "(\s|^)(%s)(\s|$)" % re.escape(item.lower())
                matches = re.findall(pat, querystring.lower())
                if matches and matches[0]:
                    qdict['lower'].append(matches[0][1])
                    qdict['normal'].append(item)

    return qdict
