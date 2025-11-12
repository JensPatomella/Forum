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
    print(username)
    print(password)

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
            session['user'] = {'username': existing_account[1]}
            return render_template("Signed-In.html")
        else:
            return redirect('/Log-In')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')