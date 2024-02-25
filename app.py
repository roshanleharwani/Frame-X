from flask import Flask, render_template, request, redirect, flash
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__)

app.config["SECRET_KEY"] = "kjsdfjsdjfsdfosfpsoifjsodfosjfosdfosjfsf"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Profile(db.Model):
    name = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(40), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=False, nullable=False)
    password = db.Column(db.String(15), nullable=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password == confirm_password:
            #     name
            #     and phone
            #     and email
            #     and password
            #     and confirm_password
            # ):

            p = Profile(name=name, phone=phone, email=email, password=password)
            db.session.add(p)
            db.session.commit()
            flash("You have signed up successfully!")
            return redirect("/internship")
        else:
            render_template("signup.html")

    return render_template("signup.html")


@app.route("/internship")
def internship():
    return render_template("internship.html")


@app.route("/apply")
def apply():
    return render_template("apply.html")


if __name__ == "__main__":
    app.run(debug=True)
