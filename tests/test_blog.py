import unittest
from app.models import Blog, Writer

class BlogModelTest(unittest.TestCase):

    def setUp(self):
        self.new_writer = Writer(fullname = "Sarah", email = "Sarahexample.com", password = "1234")
        self.new_blog = Blog(blog_message = "bla blaaah", writer = self.new_writer)
        
    def tearDown(self):
        Blog.query.delete()
        Writer.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_writer.fullname, "Sarah")
        self.assertEquals(self.new_blog.blog_message, "bla blaaah")

    def test_create_blog(self):
        self.new_blog.create_blog()
        self.assertTrue(len(Blog.query.all())>0)

    def test_get_single_blog(self):
        self.new_blog.create_blog()
        got_blog = self.new_blog.get_single_blog(self.new_blog.id)
        self.assertTrue(got_blog)

    def test_delete_blog(self):
        self.new_blog.create_blog()
        self.new_blog.delete_blog(self.new_blog.id)
        self.assertTrue(len(Blog.query.all()) == 0)