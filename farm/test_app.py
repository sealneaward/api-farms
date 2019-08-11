import unittest
from farm.app import app

class FlaskTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(FlaskTest, self).__init__(*args, **kwargs)
        self.app = app.test_client()
    def test_home_status_code(self):
        # sends HTTP GET request to route with no developed response
        result = self.app.get('/')
        # assert the status code of the response
        self.assertEqual(result.status_code, 404)

    def test_home_data(self):
        # sends HTTP GET request to the application on the supported path
        result = self.app.get('/hello?name=Neil')

        # assert the response data
        self.assertEqual(result.data.decode("utf-8"), "Hello Neil!")

if __name__ == '__main__':
    unittest.main()
