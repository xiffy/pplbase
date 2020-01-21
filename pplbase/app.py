import os
from flask import Flask, render_template, request, escape, abort, redirect, url_for, send_from_directory
from .person import Person
from .person_finder import PersonFinder


def home():
    if request.args.get('q', None):
        q = escape(request.args['q'])
    else:
        q = ''
    resultset = PersonFinder(q)
    response = resultset.execute()
    return render_template('home.html', response=response, q=q)


def delete_person(name):
    response = Person.getter(name)
    if response.success() and response.hits.total.value == 1:
        Person.delete(name)
    else:
        # fail hard
        abort(404)
    return 'He is a gonner! <a href="/">OK</a>'


def update_person(name):
    response = Person.getter(name)
    if response.success() and response.hits.total.value == 1:
        original = response.hits[0].to_dict()
        if request.method == 'POST':
            person_save(doc_id=response.hits[0].meta.id)
            return redirect(url_for('view_person', name=request.form.get('name')))
        return render_template('person-form.html', mode='update', values=original, answers=ANSWERS, questions=QUESTIONS)
    else:
        abort(404)


def view_person(name):
    response = Person.getter(name)
    if response.success() and response.hits.total.value == 1:
        original = response.hits[0].to_dict()
        return render_template('person.html', values=original, answers=ANSWERS, questions=QUESTIONS)
    else:
        return 'name %s not on file' % name


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
    # removes all empty lists from the answers
    answers = {k: v for k, v in answers.items() if len(v) != 0}
    if doc_id is None:
        newperson = Person(**answers)
        newperson.save(refresh=True)
    else:
        person = Person.get(doc_id)
        person.update(refresh=True, **answers)


def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def create_pplbase():
    app = Flask('pplbase')
    app.add_url_rule('/favicon.ico', view_func=favicon)
    app.add_url_rule('/new', methods=["GET", "POST"], view_func=add_person)
    app.add_url_rule('/view/<name>', view_func=view_person)
    app.add_url_rule('/update/<name>', methods=['GET', 'POST'], view_func=update_person)
    app.add_url_rule('/delete/<name>', methods=['GET', 'POST'], view_func=delete_person)
    app.add_url_rule('/', view_func=home)
    app.add_url_rule('/search', view_func=home)
    return app


app = create_pplbase()

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
                  'title': 'Ontwikkelt voor:'},
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
                  "Javascript", "Typescript", "XML", "HTML", "YAML", "Groovy", "Erlang", "GraphQL", "WebAssembly",
                  'Assembly'],
    'databases': ['MySQL', 'MariaDB', 'Postgres', 'SQL Server', 'SQLite', 'Oracle', 'MongoDB', 'Redis',
                  'Elasticsearch', 'SOLR', 'Cassandra', 'Neo4J', 'Firebase'],
    'web': ['jQuery', 'React', 'Angular', 'Angular.js', 'Vue.js', 'ASP.NET', 'Express', 'Spring', 'Spring Boot',
            'Django', 'Dropwizard', 'Rails', 'Java EE', 'Java SE', 'Hibernate', 'Flask'],
    'frameworks': ['Node.js', '.NET', 'Pandas', 'Unity 3D', 'React native', 'TensorFlow', 'Ansible', 'Puppet',
                   'Cordova', 'Xamarin', 'Apache Spark', 'Hadoop', 'Axon Framework', 'Torch / PyTorch',
                   'SonarCube', 'EclipseLink'],
    'platforms': ['Windows', 'Linux', 'MacOS', 'iOS', 'Android', 'Amazon webservices AWS', 'Google Cloud Platform',
                  'Microsoft Azure', 'IBM Cloud', 'GoCD', 'Heroku'],
    'buildtools': ['Maven', 'Gradle', 'Grunt', 'Ant', 'NPM', 'make', 'Niet van toepassing'],
    'editor': ['IntelliJ', 'Visual Studio Code', 'Visual Studio', 'PyCharm', 'Notepad++', 'Sublime', 'Qt Creator',
               'Vim', 'Eclipse', 'NetBeans', 'XCode', 'Android Studio', 'UltraEdit', 'emacs'],
    'os': ['Windows', 'MacOS', 'Linux', 'BSD', 'FreeBSD', 'Chrome', 'iOS', 'Android'],
    'containers': ['Enkel voor hobby', 'Voor ontwikkeling', 'Op de testomgeving', 'Op productie', 'Nooit'],
}
