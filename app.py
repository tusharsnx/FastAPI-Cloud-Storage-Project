from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/<username>")
def index(username):
	return f"<h1>html of {username}</h1>"

@app.route("/login")
def tushar():
	return f"<h1>html of a</h1>"

app.run(debug=True)