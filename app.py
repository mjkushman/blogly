"""Blogly application.
https://lessons.springboard.com/SQLAlchemy-Part-1-325f6b332e1f49cbb2c3b72f91cf73ae
"""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post
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
    if request.form["first_name"]:
        first_name = request.form["first_name"]
    else:
        first_name = user.first_name

    if request.form["last_name"]:
        last_name = request.form["last_name"]
    else:
        last_name = user.last_name

    if request.form["image_url"]:
        image_url = request.form["image_url"]
    else:
        image_url = user.image_url

    user.edit_user(first_name, last_name, image_url)

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """deletes a user from the database"""
    User.query.filter(User.id == user_id).delete()

    db.session.commit()
    return redirect("/")


# Show form to add a post for that user
@app.route("/users/<user_id>/posts/new")
def show_add_post(user_id):
    user = User.query.get(user_id)
    return render_template("add-post.html", user=user)


# Handle add form, add post and redirect to the user detail page
@app.route("/users/<user_id>/posts/new", methods=["POST"])
def handle_add_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<post_id>")
def show_post(post_id):
    """# Show a post. Show buttons to edit and delete the post"""
    post = Post.query.get(post_id)
    return render_template("post-detail.html", post=post)


@app.route("/posts/<post_id>/edit")
def edit_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""
    post = Post.query.get(post_id)
    return render_template("edit-post.html", post=post)


@app.route("/posts/<post_id>/edit", methods=["POST"])
def handle_edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view"""
    """A route to handle post edit submissions"""
    post = Post.query.get(post_id)
    if request.form["title"]:
        title = request.form["title"]
    else:
        title = post.title

    if request.form["content"]:
        content = request.form["content"]
    else:
        content = post.content

    post.edit_post(title, content)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")


@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete the post"""
    Post.query.filter(Post.id == post_id).delete()

    db.session.commit()
    return redirect("/")
