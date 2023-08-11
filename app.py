"""Blogly application.
https://lessons.springboard.com/SQLAlchemy-Part-1-325f6b332e1f49cbb2c3b72f91cf73ae
"""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "mysecurepassword"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def show_home_list():
    users = User.get_all_users()
    return render_template("home.html", users=users)


@app.route("/users/new")
def show_create_user_form():
    return render_template("add-user.html")


@app.route("/users/new", methods=["POST"])
def create_user():
    """Create a new user from the form"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()
    flash(f'{user.first_name} has been created')
    return redirect("/")


@app.route("/users/<user_id>")
def user_detail(user_id):
    user = User.query.get(user_id)
    # user_posts = Post.
    posts = user.posts
    return render_template("user-detail.html", user=user, posts=posts)


@app.route("/users/<user_id>/edit")
def show_edit_user_form(user_id):
    user = User.query.get(user_id)
    return render_template("edit-user.html", user=user)


@app.route("/users/<user_id>/edit", methods=["POST"])
def edit_user(user_id):
    user = User.query.get(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user.edit_user(first_name, last_name, image_url)

    db.session.add(user)
    db.session.commit()
    flash(f'{user.first_name} has been updated')
    return redirect(f"/users/{user.id}")


@app.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """deletes a user from the database"""
    user=User.query.get(user_id)
    User.query.filter(User.id == user_id).delete()

    db.session.commit()
    flash(f'{user.first_name} has been deleted')
    return redirect("/")


# Show form to add a post for that user
@app.route("/users/<user_id>/posts/new")
def show_add_post(user_id):
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template("add-post.html", user=user, tags=tags)


# Handle add form, add post and redirect to the user detail page
@app.route("/users/<user_id>/posts/new", methods=["POST"])
def handle_add_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    tag_ids = request.form.getlist('tags')
    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    for tag_id in tag_ids:
        tag = Tag.query.get(tag_id)
        # print(tag_id)
        new_post.tags.append(tag)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<post_id>")
def show_post(post_id):
    """# Show a post. Show buttons to edit and delete the post"""
    post = Post.query.get(post_id)
    tags = post.tags
    return render_template("post-detail.html", post=post, tags=tags)


@app.route("/posts/<post_id>/edit")
def edit_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""
    post = Post.query.get(post_id)
    all_tags = Tag.query.all()
    return render_template("edit-post.html", post=post, all_tags=all_tags)


@app.route("/posts/<post_id>/edit", methods=["POST"])
def handle_edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view"""
    """A route to handle post edit submissions"""
    post = Post.query.get(post_id)
    title = request.form["title"]    
    content = request.form["content"]
    tag_ids = request.form.getlist('tags')
    
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post.edit_post(title, content, tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")


@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete the post"""
    Post.query.filter(Post.id == post_id).delete()

    db.session.commit()
    return redirect("/")



@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    """Lists all tags, with links to the tag detail page."""
    return render_template('tags.html', tags=tags)



@app.route('/tags/<tag_id>')
def tag_detail(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get(tag_id) #selects the specific tag
    return render_template('tag-detail.html', tag=tag)



@app.route('/tags/new')
def show_add_tag():
    """Shows a form to add a new tag."""
    tags = Tag.query.all()
    return render_template('add-tag.html', tags=tags)


@app.route('/tags/new', methods=['POST'])
def handle_add_tag():
    """Process add form, adds tag, and redirect to tag list."""
    new_tag = Tag(name=request.form['name'])
    db.session.add(new_tag)
    db.session.commit()
    flash(f'{new_tag.name} created')
    return redirect('/tags')


@app.route('/tags/<tag_id>/edit')
def show_edit_tag(tag_id):
    """Show edit form for a tag."""
    tag = Tag.query.get(tag_id)
    return render_template('edit-tag.html', tag=tag)


@app.route('/tags/<tag_id>/edit', methods=['POST'])
def handle_edit_tag(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""
    tag = Tag.query.get(tag_id) #select the tag by id
    tag.edit_tag(request.form['name'])
    
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{tag.id}')


# TODO
@app.route('/tags/<tag_id>/edit', methods=['POST'])
def delete_tag(tag_id):
    """Delete a tag."""
    tag = Tag.query.get(tag_id)
    Tag.query.filter(Tag.id == tag_id).delete()
    flash(f"{tag.name} deleted")
    return redirect('/tags')