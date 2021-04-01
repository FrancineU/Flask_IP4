from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(writer_id):
    return Writer.query.get(int(writer_id))


class Quote:
    '''
    Quote class to define Quote object
    '''

    def __init__(self, id, author, quote):
        self.quote_id = id
        self.quote_author = author
        self.quote = quote

class Writer(UserMixin, db.Model):
    '''
    Writer class to create a writer model
    '''

    __tablename__ = 'writers'

    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(255)) 
    email = db.Column(db.String(255), unique = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    blogs = db.relationship('Blog', backref = 'writer', lazy = "dynamic")


    def save_writer(self):
        '''
        Function to save writer into the database
        '''
        db.session.add(self)
        db.session.commit()


    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)



class Blog(db.Model):
    '''
    Blog class to create a blog model
    '''

    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key = True)
    blog_title = db.Column(db.String(255))
    blog_message = db.Column(db.String(255))
    blog_pic_path = db.Column(db.String(255))
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    writer_id = db.Column(db.Integer, db.ForeignKey('writers.id'))
    comments = db.relationship('Comment', backref = 'blog', lazy = "dynamic")

    @classmethod
    def display_all_blogs(cls):
        '''
        Function to get all blogs from db
        '''

        all_blogs = Blog.query.all()
        return all_blogs

    def create_blog(self):
        '''
        function to create a blog
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_single_blog(cls, blog_id):
        '''
        Function to retreive single blog in the database
        '''
        return Blog.query.get(blog_id)

    @classmethod
    def update_blog(cls, id, new_message):
        '''
        Function to update a blog
        '''
        blog_to_update = Blog.query.filter_by(id = id).update({"blog_message" : new_message})
        # blog_to_update.query.update({"blog_message" : new_message})
        db.session.commit()

    @classmethod
    def delete_blog(cls, id):
        '''
        Function to delete a blog
        '''
        blog_to_delete = Blog.query.get(id)
        db.session.delete(blog_to_delete)
        db.session.commit()


    # def __repr__(self):
    #     return f'User {self.blog_message}'

class Comment(db.Model):
    '''
    Comment class to create a comment model
    '''

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(255))
    comment_message = db.Column(db.String(255))
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    def create_comment(self):
        '''
        Function to post comment of a specific blog
        '''
        
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_comment_by_id(cls, id):
        '''
        Function to retreive a specific comment from the db
        '''
        single_comment = Comment.query.get(int(id))
        return single_comment

    @classmethod
    def get_all_comment_from_blog(cls, blog_id):
        '''
        Function to retreive all comment of specific blog
        '''
        comments = Comment.query.filter_by(blog_id = blog_id).all()
        return comments

    def delete_comment(self):
        '''
        Function to delete a comment
        '''
        db.session.delete(self)
        db.session.commit()

    # def __repr__(self):
    #     return f'User {self.comment_message}'
