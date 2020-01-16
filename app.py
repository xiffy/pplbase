from flask import Flask, render_template, request, escape, abort, redirect, url_for, send_from_directory
from elasticsearch_dsl import Search
from person import Person
from person_finder import PersonFinder

app = Flask(__name__)

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

@app.route('/new', methods=["GET", "POST"])
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
    print(answers)
    if doc_id is None:
        newperson = Person(**answers)
        newperson.save(refresh=True)
    else:
        person = Person.get(doc_id)
        person.update(**answers)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
