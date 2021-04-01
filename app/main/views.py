from flask import render_template, redirect, url_for, abort, request
from .. import db, photos
from . import main
from ..models import Blog, Comment, Writer
from flask_login import login_required, current_user
from .forms import BlogRegistrationForm, CommentForm, UpdateProfile
from ..requests import get_quote

@main.route("/", methods = ["GET"])
def index():

    #Get all blogs
    all_blogs = Blog.display_all_blogs()
    random_quote = get_quote()

    return render_template('main/index.html', quote = random_quote)

@main.route('/user/<uname>', methods = ["GET"])
@login_required
def writer_profile(uname):
    writer = Writer.query.filter_by(email = uname).first()

    if writer is None:
        abort()
    
    writer_blogs = writer.blogs

    return render_template('profile/profile.html', writer = writer, blogs = writer_blogs)

@main.route('/writer/update/profile/pic/<uname>', methods = ["POST"])
@login_required
def update_writer_pic(uname):

    writer = Writer.query.filter_by(email = uname).first()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = 'photos/' + filename
        writer.profile_pic_path = path

        db.session.commit()

    return redirect(url_for('.writer_profile', uname = writer.email))

@main.route('/user/profile/update/<uname>', methods = ["GET", "POST"])
@login_required
def update_profile(uname):
    writer = Writer.query.filter_by(email = uname).first()

    if writer is None:
        abort()

    form = UpdateProfile()
    if form.validate_on_submit():
        writer.bio = form.bio.data 

        db.session.add(writer)
        db.session.commit()

        return redirect(url_for('.writer_profile', uname = writer.email))

    return render_template('profile/update-profile-form.html', update_profile_form = form)
     
    
@main.route('/blog/new', methods = ['GET', 'POST'])
@login_required
def save_new_blog():

    form = BlogRegistrationForm()

    if form.validate_on_submit():
        new_blog = Blog(blog_title = form.blog_title.data ,blog_message = form.blog_message.data, writer = current_user)
        new_blog.create_blog()

        return redirect(url_for('main.writer_profile', uname = current_user.email))

    return render_template('main/new-blog.html', blog_form = form)

@main.route('/blog/update/pic/<int:id>', methods = ["POST"])
@login_required
def update_blog_pic(id):
    blog = Blog.query.filter_by(id = id).first()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = 'photos/' + filename
        blog.blog_pic_path = path

        db.session.commit()
    
    return redirect(url_for('.display_single_blog', id = blog.id))

@main.route('/blog/all', methods = ["GET"])
def get_all_blogs():

    #Get all blogs
    all_blogs = Blog.display_all_blogs()

    return render_template('main/blog-list.html', blogs = all_blogs)


@main.route('/blog/<int:id>', methods = ["GET", "POST"])
def display_single_blog(id):

    single_blog = Blog.get_single_blog(id)
    print(single_blog.blog_title)

    if single_blog is None:
        abort(404)

    else:
        blog_comments = single_blog.comments
        form = CommentForm()

        if form.validate_on_submit():
            comment = Comment(user_name = form.user_name.data, comment_message = form.comment.data, blog = single_blog)
            comment.create_comment()

            return redirect(url_for('main.display_single_blog', id = single_blog.id))

    return render_template('main/single-blog.html', blog = single_blog, comments = blog_comments, comment_form = form)


@main.route('/blog/update/<int:id>', methods = ['GET', 'POST'])
@login_required
def update_blog(id):

    form = BlogRegistrationForm()

    if form.validate_on_submit():
        blog_to_update = Blog.get_single_blog(id)
        if blog_to_update is not None:
            # blog_to_update.update_blog(id, form.blog_message.data)
            blog_to_update.blog_message = form.blog_message.data
            blog_to_update.blog_title = form.blog_title.data
            db.session.add(blog_to_update)
            db.session.commit()
            return redirect(url_for('main.display_single_blog', id = blog_to_update.id))
        else :
            abort(404)

    return render_template('main/update-blog.html', blog_form = form)
    

@main.route('/blog/delete/<int:id>', methods = ['GET'])
@login_required
def delete_blog(id):
    Blog.delete_blog(id)
    return redirect(url_for('main.writer_profile', uname = current_user.email))


@main.route('/blog/comment/<int:id>', methods = ['GET', 'POST'])
def add_comment(id):

    form = CommentForm()

    if form.validate_on_submit():
        blog = Blog.get_single_blog(id)
        if blog is not None:
            comment = Comment(user_name = form.user_name.data, comment_message = form.comment.data, blog = blog)
            comment.create_comment()

            return redirect(url_for('main.display_single_blog', id = blog.id))

        else :
            abort(404)
    
    return render_template('main/comment-form.html', comment_form = form)


@main.route('/comment/delete/<int:id>', methods = ['GET'])
@login_required
def delete_comment(id):
    comment = Comment.get_comment_by_id(id)
    blog_id = comment.blog_id
    comment.delete_comment()

    return redirect(url_for('.display_single_blog', id = blog_id))
