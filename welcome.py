

from flask import Flask, render_template, redirect, url_for, abort, request, flash, session
from .user_models import create_user_table, get_user, insert_user
import random, math

from .decorators import welcome_screen, login_required
from .post_models import (
    create_post_table,
    get_posts,
    find_post,
    random_post,
    insert_post,
    count_posts,
    paginated_posts,
)

app = Flask(__name__)

######## SET THE SECRET KEY ###############
# You can write random letters yourself or
# Go to https://randomkeygen.com/ and select a
# random secret key
####################
app.secret_key = "thrwiotbrjwpfhwfjeipmisprjerptitreievwiedn42945"

posts_per_page = 3

my_user = {
    'email': 'name@email.com',
    'password': 'gobblegobbleglopglop'
}

with app.app_context():
    create_post_table()
    create_user_table()
    user_exist = get_user(my_user['email'], my_user['password'])
    if not user_exist:
        insert_user(my_user['email'], my_user['password'])


@app.route("/")
@welcome_screen
def home_page():
    total_posts = count_posts()
    pages = math.ceil(total_posts / posts_per_page)
    current_page = request.args.get("page", 1, int)
    posts_data = paginated_posts(current_page, posts_per_page)
    return render_template(
        "page.html",
        posts=posts_data,
        current_page=current_page,
        total_posts=total_posts,
        pages=pages,
    )


@app.route("/welcome")
def welcome_page():
    return render_template("welcome.html")


@app.route("/<post_link>")
@welcome_screen
def post_page(post_link):
    post = find_post(post_link)
    if post:
        return render_template("post.html", post=post)
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


@app.route("/random")
def random_post_page():
    post = random_post()
    return redirect(url_for("post_page", post_link=post["permalink"]))


@app.route("/new-post", methods=["GET", "POST"])
@login_required
def new_post():
    if request.method == "GET":
        return render_template("newpost.html", post_data={})
    else:
        post_data = {
            "title": request.form["post-title"],
            "author": request.form["post-author"],
            "content": request.form["post-content"],
            "permalink": request.form["post-title"].replace(" ", "-"),
            "tags:": request.form["post-tags"],
        }

        existing_post = find_post(post_data["permalink"])
        if existing_post:
            app.logger.warning(f"duplicate post: {post_data['title']}")
            flash(
                "error", "There's already a similar post, maybe use a different title"
            )
            return render_template("newpost.html")
        else:
            insert_post(post_data)
            app.logger.info(f"new post: {post_data['title']}")
            flash("success", "Congratulations on publishing another blog post.")
            return redirect(url_for("post_page", post_link=post_data["permalink"]))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email-id']
        password = request.form['password']
        user = get_user(email, password)
        if user:
            session['logged_in'] = True
            flash('success', 'You are now logged in.')
            return redirect(url_for('home_page'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('login.html')
