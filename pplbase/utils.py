# Helper functions
import re

# re-find the used Keywords in the query string.
# the regular expression only catches full phrases. (So selecting 'Java' won't select 'Javascript' as well)
def decompose_querystring(response=None, querystring=None):
    """
    Decompose the querystring back into keywords known in the facets 
    Only full phrases are considered (hence the \b)
    Keyword Arguments: 
    response - he elasticsearch-dsl response object
    querystring - the querystring from the URL """
    qlist = []
    if response and querystring:
        for term in response.facets:
            for item, _, _ in response.facets[term]:
                #print(term, end=': ')
                #print(response.facets[term])
                qlist.extend(re.compile(r"\b%s\b" % re.escape(item.lower())).findall(querystring.lower()))
    return qlist
