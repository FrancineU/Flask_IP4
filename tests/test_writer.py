import unittest
from app.models import Writer

class WriterModelTest(unittest.TestCase):

    def setUp(self):
        self.new_writer = Writer(password = '123')
    
    def test_password_setter(self):
        self.assertTrue(self.new_writer.pass_secure is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_writer.password
        
    def test_password_verification(self):
        self.assertTrue(self.new_writer.verify_password('123'))