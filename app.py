from flask import Flask,  render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
	return render_template("index.html")

@app.route("/login")
def tushar():
	return f"<h1>html of a</h1>"

app.run(debug=True)