from flask import Flask, render_template, request, escape, abort, redirect, url_for
from elasticsearch_dsl import FacetedSearch, TermsFacet, connections, UpdateByQuery, \
    Document, Text, Keyword, normalizer, Search


connections.create_connection()

app = Flask(__name__)

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

# dit moet eenmalig om de index correct aan te maken:
Person.init()

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

@app.route('/')
@app.route('/search')
def hello_world():
    if request.args.get('q', None):
        q = escape(request.args['q'])
    else:
        q = ''
    resultset = PersonFinder(q)
    response = resultset.execute()
    return render_template('home.html', response=response, q=q)


@app.route('/delete/<name>')
def delete_person(name):
    pers = Search(index='softwareprofs').query("match", name=name)
    response = pers.execute()
    if response.success() and response.hits.total.value == 1:
        pers.delete()
    else:
        # fail hard
        abort(404)
    return 'He is a gonner! <a href="/">OK</a>'

@app.route('/update/<name>', methods=['GET', 'POST'])
def update_person(name):
    pers = Search(index='softwareprofs').query("match", name=name)
    response = pers.execute()
    if response.success() and response.hits.total.value == 1:
        original = response.hits[0].to_dict()
        if request.method == 'POST':
            person_save(doc_id=response.hits[0].meta.id)
            return redirect(url_for('view_person', name=request.form.get('name')))
        return render_template('person-form.html', mode='update', values=original, answers=ANSWERS, questions=QUESTIONS)
    else:
        abort(404)

@app.route('/view/<name>')
def view_person(name):
    pers = Search(index='softwareprofs').query("match", name=name)
    response = pers.execute()
    if response.success() and response.hits.total.value == 1:
        original = response.hits[0].to_dict()
        return render_template('person.html', values=original, answers=ANSWERS, questions=QUESTIONS)
    else:
        return str(response)

@app.route('/nieuw', methods=["GET", "POST"])
def add_person():
    if request.method == 'POST':
        person_save()
        return redirect(url_for('view_person', name=request.form.get('name')))
    return render_template('person-form.html', mode='new', values={}, answers=ANSWERS, questions=QUESTIONS)


def person_save(doc_id=None):
    answers = {'name': escape(request.form.get('name', None))}
    for field in QUESTIONS:
        answers[field] = request.form.getlist(field)
        if QUESTIONS[field].get('extra', False):
            extra = request.form.get('%s_extra' % field, None)
            if extra:
                answers[field].extend(extra.split(','))
    print(answers)
    if doc_id is None:
        newperson = Person(**answers)
        newperson.save(refresh=True)
    else:
        person = Person.get(doc_id)
        person.update(**answers)


if __name__ == '__main__':
    Person.init()
    app.run()


QUESTIONS = {
    'languages': {'q': 'Welke talen gebruik je veelal (programmeren, scripten, markup)?',
                  'extra': True,
                  'title': 'Programmeert, script en markupt in:'},
    'databases': {'q': 'Wat voor Database(s) gebruik je veelal?',
                  'extra': True,
                  'title': 'Bewaard in:'},
    'web': {'q': 'Welke web frameworks gebruik je veelal?',
            'extra': True,
            'title': 'Op poort 80 antwoord:'},
    'frameworks': {'q': 'Welke andere frameworks, libraries en/of tools gebruik je veelal?',
                   'extra': True,
                   'title': 'Gebruikt ook'},
    'platforms': {'q': 'Wat voor platform(s) ontwikkel je veelal tegen?',
                  'extra': True,
                  'title':'Ontwikkelt voor:'},
    'buildtools': {'q': 'Wat voor build tools gebruik je veelal?',
                   'extra': True,
                   'title': 'Build met:'},
    'editor': {'q': 'Wat voor applicatie gebruik je veelal voor software ontwikkeling?',
               'extra': True,
               'title': 'Typt in:'},
    'os': {'q': 'Welk OS draai je momenteel?',
           'extra': False,
           'title': 'Op:'},
    'containers': {'q': 'Maak je gebruik van containers?',
                   'extra': False,
                   'title': 'eh Containers?'},
}

ANSWERS = {
    'languages': ['Java', 'Kotlin', 'Python', 'PHP', '.NET', "C", "C++", "C#", "Objective C", "Ruby", "Go", "Scala",
                  "Javascript", "Typescript", "XML", "HTML", "YAML", "Groovy", "Erlang", "GraphQL", "WebAssembly"],
    'databases': ['MySQL', 'MariaDB', 'Postgres', 'SQL Server', 'SQLite', 'Oracle', 'MongoDB', 'Redis',
                  'Elasticsearch', 'SOLR', 'Cassandra', 'Neo4J', 'Firebase'],
    'web': ['jQuery', 'React', 'Angular', 'Vue.js', 'ASP.NET', 'Express', 'Spring', 'Spring Boot', 'Django',
            'Dropwizard', 'Rails', 'Java EE'],
    'frameworks': ['Node.js', '.NET', 'Pandas', 'Unity 3D', 'React native', 'TensorFlow', 'Ansible', 'Puppet',
                   'Cordova', 'Xamarin', 'Apache Spark', 'Hadoop', 'Axon Framework', 'Torch / PyTorch',
                   'SonarCube'],
    'platforms': ['Windows', 'Linux', 'MacOS', 'iOS', 'Android', 'Amazon webservices AWS', 'Google Cloud Platform',
                  'Microsoft Azure', 'IBM Cloud', 'GoCD', 'Heroku'],
    'buildtools': ['Maven', 'Gradle', 'Grunt', 'Ant', 'NPM', 'Niet van toepassing'],
    'editor': ['IntelliJ', 'Visual Studio Code', 'Visual Studio', 'PyCharm', 'Notepad++', 'Sublime', 'Qt Creator',
                'Vim', 'Eclipse', 'NetBeans', 'XCode', 'Android Studio', 'UltraEdit'],
    'os': ['Windows', 'MacOS', 'Linux', 'Chrome', 'iOS', 'Android'],
    'containers': ['Enkel voor hobby', 'Voor ontwikkeling', 'Op de testomgeving', 'Op productie', 'Nooit'],
}
