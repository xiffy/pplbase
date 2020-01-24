from elasticsearch_dsl import FacetedSearch, TermsFacet, connections, Search

class PersonFinder(FacetedSearch):
    index = 'softwareprofs'
    fields = ['_all']
    facets = {
        'languages': TermsFacet(field='languages.raw'),
        'web': TermsFacet(field='web.raw'),
        'frameworks': TermsFacet(field='frameworks.raw'),
        'databases': TermsFacet(field='databases.raw'),
        'platforms': TermsFacet(field='platforms.raw'),
        'buildtools': TermsFacet(field='buildtools.raw'),
        'editor': TermsFacet(field='editor.raw'),
        'os': TermsFacet(field='os.raw'),
        'containers': TermsFacet(field='containers.raw')
    }
    def search(self):
        s = super().search()
        if not self._query:
            return s.query('match_all')
        return s.query('multi_match', query=self._query, operator="AND", fields="_all")

