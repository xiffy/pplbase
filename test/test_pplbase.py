import unittest
from pplbase.app import create_pplbase

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
        Dit moet opgesplitst worden in atomaire acties zodra er een dedicated (schone)
        elasticsearch wordt opgestart voor het testen.
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
        })
        self.assertEqual(response.status_code, 302)
        assert '/view/Test%20de%20Kees' in str(response.data)

        response = self.app.get('/update/Test de Kees')
        assert 'Oracle' in str(response.data)

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
        response = self.app.get('/', query_string="q=*")
        self.assertEqual(response.status_code, 200)
        assert 'Vind!' in str(response.data)









if __name__ == "__main__":
    unittest.main()
