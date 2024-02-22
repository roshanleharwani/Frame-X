from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/internship")
def internship():
    return render_template("internship.html")


@app.route("/apply")
def apply():
    return render_template("apply.html")


if __name__ == "__main__":
    app.run()
