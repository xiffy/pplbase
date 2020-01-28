import unittest
from attrdict import AttrDict
from pplbase.app import create_pplbase
from pplbase.person import Person
from pplbase.person_finder import PersonFinder
from pplbase.utils import decompose_querystring


class TestPerson(unittest.TestCase):
    def test_personfinder(self):
        result = PersonFinder('Steve Jobs').execute()
        self.assertEqual(len(result), 1)
        self.assertGreater(len(result.facets.to_dict()), 0)
        self.assertIn('Java', result[0].languages)

    def test_person_getter(self):
        result = Person.getter('Steve Jobs')
        self.assertEqual(len(result), 1)

class TestRoutes(unittest.TestCase):

    def setUp(self):
        app = create_pplbase()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_add_new(self):
        response = self.app.get('/new')
        self.assertEqual(response.status_code, 200)

    def test_post_add_new_update_and_delete(self):
        """
        Test een roundtrip van een persoon;
        - Insert a person into Elastic,
        - Get person for update,
        - Update person,
        - View person,
        - Delete person
        """
        response = self.app.post('/new', data={
            'name': 'Test de Kees',
            'languages': ['Java', 'Kotlin', 'PHP'],
            'databases': ['MariaDB', 'MySQL', 'Postgres', 'Oracle'],
            'web': ['React'],
            'frameworks': ['Pandas'],
            'platforms': ['Windows', 'Android'],
            'buildtools': ['make', 'Maven'],
            'editor': ['PyCharm'],
            'os': ['Windows', 'Linux'],
            'containers': ['nooit'],
            'pet_peeves': ['SCO Unix, Novell'],
            'wanna_learns': ['Docker', 'Kubernetes'],
        })
        self.assertEqual(response.status_code, 302)
        assert '/view/Test%20de%20Kees' in str(response.data)

        response = self.app.get('/update/Test de Kees')
        assert 'Oracle' in str(response.data)
        assert 'SCO Unix' in str(response.data)

        response = self.app.post('/update/Test de Kees', data={
            'name': 'Test de Kees',
            'languages': ['Java', 'Kotlin'],
            'databases': ['MariaDB', 'MySQL', 'Postgres'],
            'web': ['React'],
            'frameworks': ['Pandas', 'Hadoop'],
            'platforms': ['Windows', 'Android'],
            'buildtools': ['make', 'Maven'],
            'editor': ['PyCharm'],
            'os': ['Windows', 'Linux'],
            'containers': ['nooit'],
        })
        self.assertEqual(response.status_code, 302)
        assert '/view/Test%20de%20Kees' in str(response.data)

        response = self.app.get('/view/Test de Kees')
        assert 'PHP' not in str(response.data)
        assert 'Hadoop' in str(response.data)

        response = self.app.get('/delete/Test de Kees')
        assert 'gonner' in str(response.data)

    def test_get_view_person(self):
        response = self.app.get('/view/Bill Gates')
        self.assertEqual(response.status_code, 200)
        assert 'Bill Gates' in str(response.data)

    def test_favicon(self):
        response = self.app.get('/favicon.ico')
        self.assertEqual(response.headers.get('Content-type', None), 'image/vnd.microsoft.icon')
        response.close()

class TestUtils(unittest.TestCase):
    response = AttrDict({'facets': {'languages': [('Java', 3, False),
                                                  ('XML', 2, False),
                                                  ('YAML', 2, False),
                                                  ('Assembly', 1, False),
                                                  ('C++', 1, False),
                                                  ('C', 1, False),
                                                  ('C#', 1, False),
                                                  ('Go', 1, False),
                                                  ('Groovy', 1, False),
                                                  ('HTML', 1, False),
                                                  ('Javascript', 1, False),
                                                  ('Kotlin', 1, False)],
                                    'web': [('Hibernate', 3, False),
                                            ('Java EE', 2, False),
                                            ('Java SE', 2, False),
                                            ('jQuery', 2, False),
                                            ('Angular', 1, False),
                                            ('Dropwizard', 1, False)],
                                    'editor': [('Eclipse', 2, False),
                                               ('IntelliJ', 2, False),
                                               ('Sublime', 2, False),
                                               ('NetBeans', 1, False)],
                                    'os': [('Windows', 2, False),
                                           ('Android', 1, False),
                                           ('Linux', 1, False),
                                           ('MacOS', 1, False)],
                                    'databases': [('MongoDB', 3, False),
                                                  ('Oracle', 3, False),
                                                  ('Postgres', 3, False),
                                                  ('Redis', 2, False),
                                                  ('MariaDB', 1, False),
                                                  ('MySQL', 1, False),
                                                  ('SQLite', 1, False)]
                                    }
                         })

    def test_decompose_empty_querystring(self):
        q = ''
        self.assertListEqual(decompose_querystring(response=self.response, querystring=q), [])

    def test_decompose_single_kw_querystring(self):
        q = 'JAVA'
        self.assertListEqual(decompose_querystring(response=self.response, querystring=q), ['java'])

    def test_decompose_triple_c_querystring(self):
        q = 'c C++ c#'
        self.assertListEqual(decompose_querystring(response=self.response, querystring=q), ['c++', 'c', 'c#'])

    def test_decompose_some_kw_querystring(self):
        q ="ORACLE mysql scalar clojure"
        self.assertListEqual(decompose_querystring(response=self.response, querystring=q), ['oracle', 'mysql'])


if __name__ == "__main__":
    unittest.main()
