from elasticsearch_dsl import connections, Document, Text, Keyword, normalizer, Index


connections.create_connection()

lowercase = normalizer('lowercaser',
    filter=['lowercase']
)


class Person(Document):
    name = Text(analyzer='snowball', copy_to='_all')
    languages = Keyword(normalizer=lowercase, copy_to='_all')
    web = Keyword(normalizer=lowercase, copy_to='_all')
    frameworks = Keyword(normalizer=lowercase, copy_to='_all')
    databases = Keyword(normalizer=lowercase, copy_to='_all')
    platforms = Keyword(normalizer=lowercase, copy_to='_all')
    buildtools = Keyword(normalizer=lowercase, copy_to='_all')
    editor = Keyword(normalizer=lowercase, copy_to='_all')
    os = Keyword(normalizer=lowercase, copy_to='_all')
    containers = Keyword(normalizer=lowercase, copy_to='_all')
    wanna_learns = Keyword(normalizer=lowercase, copy_to='_all')
    pet_peeves = Keyword(normalizer=lowercase, copy_to='_all')
    _all = Text(analyzer='snowball')
    class Index:
        name = 'softwareprofs'


if not Index('softwareprofs').exists():
    # dit moet eenmalig om de index correct aan te maken:
    Person.init()