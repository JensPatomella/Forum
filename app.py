from flask import Flask, render_template, session, redirect, url_for, request, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'abc'

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="", 
  database="webbserverprogrammering"
)
mycursor = mydb.cursor()

def is_logged_in():
    if 'user' not in session:
        return False
    user_id = session['user'].get('id')
    if not user_id:
        return False
    mycursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    user = mycursor.fetchone()
    if user:
        return True
    else:
        session.pop('user', None)
        return False

@app.route("/")
def index():
    if is_logged_in():
        return redirect(url_for('forum'))
    else:
        return render_template("index.html")

@app.route("/Log-In", methods=["GET", "POST"])
def log():
    return render_template("Log-In.html")

@app.route("/Create-Account", methods=["GET","POST"])
def create():
    return render_template("Create-Account.html")

@app.route("/Account-Created", methods=["POST"])
def createdaccount():
    username = request.form.get('Username', '')
    password = request.form.get('Password', '')

    mycursor.execute("SELECT * FROM users WHERE username = (%s)", (username,))
    existing_user = mycursor.fetchone()
    if existing_user:
        return redirect(url_for('create'))
    else:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template("Account-Created.html")

@app.route('/Signed-In', methods=['POST'])
def signed():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        existing_account = mycursor.fetchone()
        print(existing_account)
        if existing_account:
            session['user'] = {'id': existing_account[0], 'username': existing_account[1]}
            return redirect(url_for('forum'))
        else:
            return redirect('/Log-In')

@app.route('/forum')
def forum():
    mycursor.execute("""
    SELECT posts.id, posts.title, posts.content, posts.topic, posts.created_at, users.username 
    FROM posts 
    JOIN users ON posts.user_id = users.id
    WHERE posts.parent_post_id IS NULL
    ORDER BY posts.created_at DESC
    """)
    posts = mycursor.fetchall()
    posts_list = []
    for post in posts:
        posts_list.append({
            'id': post[0],
            'title': post[1],
            'content': post[2],
            'topic': post[3],
            'created_at': post[4],
            'username': post[5]
        })
    return render_template('forum.html', posts=posts_list)

@app.route('/forum/new', methods=['GET', 'POST'])
def new_post():
    if 'user' not in session:
        return redirect(url_for('log'))
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        topic = request.form.get('topic')

        user_id = session['user']['id']
        sql = "INSERT INTO posts (title, content, user_id, topic) VALUES (%s, %s, %s, %s)"
        val = (title, content, user_id, topic)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('forum'))
    else:
        return redirect(url_for('forum'))

@app.route('/post/<int:post_id>')
def view_post(post_id):
    mycursor.execute("""
        SELECT posts.id, posts.title, posts.content, posts.topic, posts.created_at, users.username 
        FROM posts 
        JOIN users ON posts.user_id = users.id
        WHERE posts.id = %s
    """, (post_id,))
    post = mycursor.fetchone()
    if not post:
        return "Post not found", 404
    main_post = {
        'id': post[0],
        'title': post[1],
        'content': post[2],
        'topic': post[3],
        'created_at': post[4],
        'username': post[5]
    }
    mycursor.execute("""
        SELECT posts.id, posts.title, posts.content, posts.topic, posts.created_at, users.username 
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.parent_post_id = %s
        ORDER BY posts.created_at ASC
    """, (post_id,))
    comments = mycursor.fetchall()
    comments_list = []
    for comment in comments:
        comments_list.append({
            'id': comment[0],
            'title': comment[1],
            'content': comment[2],
            'topic': comment[3],
            'created_at': comment[4],
            'username': comment[5]
        })
    return render_template('post.html', post=main_post, comments=comments_list)

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'user' not in session:
        return redirect(url_for('log'))
    content = request.form.get('content')
    user_id = session['user']['id']
    title = request.form.get('title', '')
    sql = "INSERT INTO posts (title, content, user_id, parent_post_id) VALUES (%s, %s, %s, %s)"
    val = (title, content, user_id, post_id)
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for('view_post', post_id=post_id))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')