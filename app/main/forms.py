from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, SubmitField
from wtforms.validators import Required

class BlogRegistrationForm(FlaskForm):
    blog_title = StringField('Blog Title', validators = [Required()])
    blog_message = TextAreaField('Blog Message', validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    user_name = StringField('Your name', validators = [Required()])
    comment = TextAreaField('Your Comment', validators = [Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Your Bio', validators = [Required()])
    submit = SubmitField('Submit')

