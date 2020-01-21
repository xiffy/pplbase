from elasticsearch_dsl import FacetedSearch, TermsFacet, connections

class PersonFinder(FacetedSearch):
    index = 'softwareprofs'
    fields = ['_all']
    facets = {
        'languages': TermsFacet(field='languages'),
        'web': TermsFacet(field='web'),
        'frameworks': TermsFacet(field='frameworks'),
        'databases': TermsFacet(field='databases'),
        'platforms': TermsFacet(field='platforms'),
        'buildtools': TermsFacet(field='buildtools'),
        'editor': TermsFacet(field='editor'),
        'os': TermsFacet(field='os'),
        'containers': TermsFacet(field='containers')
    }
    def search(self):
        s = super().search()
        if not self._query:
            return s.query('match_all')
        return s.query('multi_match', query=self._query, operator="and", fields="_all")