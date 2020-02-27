from elasticsearch_dsl import Document, Text, Keyword, normalizer, Index, Search
from elasticsearch_dsl.query import MultiMatch, MatchPhrase, MatchAll
from elasticsearch_dsl.utils import AttrList


lowercase = normalizer('lowercaser',
                       filter=['lowercase']
                       )


class Person(Document):
    name = Text(analyzer='snowball',
                copy_to='_all')
    languages = Keyword(normalizer=lowercase, fields={'raw': Keyword()}, copy_to='_all')
    web = Keyword(normalizer=lowercase, copy_to='_all', fields={'raw': Keyword()})
    frameworks = Keyword(normalizer=lowercase, copy_to='_all', fields={'raw': Keyword()})
    databases = Keyword(normalizer=lowercase, fields={'raw': Keyword()}, copy_to='_all')
    platforms = Keyword(normalizer=lowercase, fields={'raw': Keyword()}, copy_to='_all')
    buildtools = Keyword(normalizer=lowercase, fields={'raw': Keyword()}, copy_to='_all')
    editor = Keyword(normalizer=lowercase, fields={'raw': Keyword()}, copy_to='_all')
    os = Keyword(normalizer=lowercase, fields={'raw': Keyword()}, copy_to='_all')
    containers = Keyword(normalizer=lowercase, fields={'raw': Keyword()}, copy_to='_all')
    wanna_learns = Keyword(normalizer=lowercase, fields={'raw': Keyword()})
    pet_peeves = Keyword(normalizer=lowercase, fields={'raw': Keyword()})
    _all = Text(analyzer='snowball')

    class Index:
        name = 'softwareprofs'
        settings = {'number_of_replicas': 0}

    @classmethod
    def getter(cls, name):
        q = [w for w in name.split(' ')]
        pers = Search(index='softwareprofs').query("simple_query_string", query=' +'.join(q), fields=["name"])
        return pers.execute()

    @classmethod
    def delete(cls, name):
        q = [w for w in name.split(' ')]
        pers = Search(index='softwareprofs').query("simple_query_string", query=' +'.join(q), fields=["name"])
        pers.delete()
        return True

    @classmethod
    def suggest(cls, txt):
        p = cls.search()
        p.query = MultiMatch(query=txt,
                             type='bool_prefix',
                             fields=['name'])
        return p.execute()

    @classmethod
    def name_unique(cls, txt):
        p = cls.search()
        p.query = MatchPhrase(name=txt)
        return p.execute()

    @classmethod
    def all(cls):
        p = cls.search()
        p.query = MatchAll()
        return p.execute()

    def dictit(self):
        pers = {'name': self.name}
        for fld in self:
            if isinstance(self[fld], AttrList):
                pers[fld] = list(self[fld])
            else:
                pers[fld] = self[fld]
        return pers




if not Index('softwareprofs').exists():
    # dit moet eenmalig om de index correct aan te maken:
    Person.init()
