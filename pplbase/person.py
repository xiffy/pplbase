from elasticsearch_dsl import Document, Text, Keyword, normalizer, Index, Search

lowercase = normalizer('lowercaser',
                       filter=['lowercase']
                       )


class Person(Document):
    name = Text(analyzer='snowball', copy_to='_all')
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


if not Index('softwareprofs').exists():
    # dit moet eenmalig om de index correct aan te maken:
    Person.init()
