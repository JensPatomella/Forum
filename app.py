from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Log-In")
def about():
    return render_template("Log-In.html")

@app.route("/Create-Account")
def contact():
    return render_template("Create-Account.html")

@app.route('/Signed-In', methods=['POST'])
def write():
    return render_template("Signed-In.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')