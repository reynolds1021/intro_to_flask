from . import bp as blog
from flask import request, url_for, render_template, flash, redirect
from app import db
from flask_login import current_user, login_required
from app.models import Post
from .forms import BlogPostForm


@blog.route('/createposts', methods=['GET', 'POST'])
@login_required
def createposts():
    form = BlogPostForm()
    context = {
        'form': form
    }
    if request.method == 'POST' and form.validate():
        # Get Information
        title = form.title.data
        content = form.content.data
        user_id = current_user.id

        # Create new instance of Post
        new_post = Post(title, content, user_id)

        # Add post to db
        db.session.add(new_post)
        db.session.commit()

        # flash success message
        flash("You have successfully created a new post", 'success')

        return redirect(url_for('blog.createposts'))

    return render_template('createposts.html', **context)


@blog.route('/posts/<int:post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@blog.route('/posts/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    update_form = BlogPostForm()
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST' and update_form.validate():
        title = update_form.title.data
        content = update_form.content.data
        user_id = current_user.id 

        post.title = title
        post.content = content
        post.user_id = user_id

        db.session.commit()
        return redirect(url_for('blog.post_update', post_id=post.id))

    return render_template('post_update.html', form=update_form, post=post)


@blog.route('/posts/delete/<int:post_id>', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))