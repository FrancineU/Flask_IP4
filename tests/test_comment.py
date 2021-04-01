import unittest
from app.models import Comment, Blog, Writer

class CommentModelTest(unittest.TestCase):
    
    def setUp(self):
        self.new_writer = Writer(fullname = "Sarah", email = "Sarah@example.com", password = "1234")
        self.new_blog = Blog(blog_message = "bla blaaah", writer = self.new_writer)
        self.new_comment = Comment(user_name = "Uwera", comment_message = "Great", blog = self.new_blog)

    def tearDown(self):
        Comment.query.delete()
        Blog.query.delete()
        Writer.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_writer.fullname, "Sarah")
        self.assertEquals(self.new_blog.blog_message, "bla blaaah")
        self.assertEquals(self.new_comment.comment_message, "Great")

    def test_create_comment(self):
        self.new_comment.create_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_get_comment_by_id(self):
        self.new_comment.create_comment()
        gotten_comment = self.new_comment.get_comment_by_id(self.new_comment.id)
        self.assertTrue(gotten_comment)

    def test_delete_comment(self):
        self.new_comment.create_comment()
        comment_to_delete = Comment.get_comment_by_id(self.new_comment.id)
        comment_to_delete.delete_comment()
        self.assertTrue(len(Comment.query.all()) == 0)
    