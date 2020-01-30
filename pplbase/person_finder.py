from elasticsearch_dsl import FacetedSearch, TermsFacet, connections, Search

class PersonFinder(FacetedSearch):
    """Performs a faceted search on elastic,
    defines the facets in use,
    which field(s) to search in
    and by overriding search perform the search """
    index = 'softwareprofs'
    fields = ['_all']
    facets = {
        'languages': TermsFacet(field='languages.raw', size=20),
        'web': TermsFacet(field='web.raw', size=20),
        'frameworks': TermsFacet(field='frameworks.raw', size=20),
        'databases': TermsFacet(field='databases.raw', size=20),
        'platforms': TermsFacet(field='platforms.raw', size=20),
        'buildtools': TermsFacet(field='buildtools.raw', size=20),
        'editor': TermsFacet(field='editor.raw', size=20),
        'os': TermsFacet(field='os.raw', size=20),
        'containers': TermsFacet(field='containers.raw', size=20)
    }
    def search(self):
        s = super().search()
        if not self._query:

            return s.query('match_all')
        return s.query('multi_match', query=self._query, operator="AND", fields="_all")

