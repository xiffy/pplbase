# Helper functions
import re

def decompose_querystring(response=None, querystring=None):
    """
    Decompose the querystring back into keywords known in the facets 
    Only full phrases are considered (hence the \s (any whitespace, trumps \b in this case)

    Keyword Arguments: 
    response - the elasticsearch-dsl response object
    querystring - the querystring from the URL

    Return value:
    dict -lower: list (found keywords in lowercase)
         -normal: list (found keywords in normal casing)
         -input: remainder of he querystring as a string """
    qdict = {'lower': [],
             'normal': [],
             'input': querystring}
    if response and querystring:
        for term in response.facets:
            for item, _, _ in response.facets[term]:
                pat = "(\s|^)(%s)(\s|$)" % re.escape(item.lower())
                matches = re.findall(pat, querystring.lower())
                if matches and matches[0]:
                    qdict['lower'].append(matches[0][1])
                    qdict['normal'].append(item)
                    qdict['input'] = re.sub(pat, ' ', qdict['input'], flags=re.IGNORECASE).strip()
    # make keywords unique
    qdict['normal'] = sorted(list(set(qdict['normal'])))
    qdict['lower'] = sorted(list(set(qdict['lower'])))
    return qdict
