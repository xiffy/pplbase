import unittest
import pplbase.person
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

    def test_post_add_new(self):
        response = self.app.post('/new', data={
            'name': 'Test de Kees',
            'languages': ['Java', 'Kotlin', 'PHP'],
            'databases': ['MariaDB', 'MySQL', 'Postgres'],
            'web': ['React'],
            'frameworks': ['Pandas'],
            'platforms': ['Windows', 'Android'],
            'buildtools': ['make', 'Maven'],
            'editor': ['PyCharm'],
            'os': ['Windows', 'Linux'],
            'containers': ['nooit'],
        })
        print(str(response.data))

    def test_delete_person(self):
        pass

    def test_get_update_person(self):
        pass

    def test_get_view_person(self):
        response = self.app.get('/', query_string="q=*")
        self.assertEqual(response.status_code, 200)
        assert 'Vind!' in str(response.data)









if __name__ == "__main__":
    unittest.main()
