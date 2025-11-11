from flask import Flask, render_template, session, redirect, url_for, request
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Add secret key for session management

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="", 
  database="webbserverprogrammering"
)
mycursor = mydb.cursor()

@app.route("/")
def index():
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

    mycursor.execute("SELECT * FROM users WHERE username = '{username}'")
    if mycursor.rowcount > 0:
        return redirect(url_for('create'))#problem typ här fixa
    else:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template("Account-Created.html")


@app.route('/Signed-In', methods=['POST'])
def signed():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        mycursor.execute("SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        users = mycursor.fetchone()
        for user in users:
            if user[1] == username and user[2] == password:
                session['username'] = username
                return redirect(url_for('signed'))
        else:
            return render_template("Log-In.html", error="Invalid credentials")
    return render_template("Signed-In.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')