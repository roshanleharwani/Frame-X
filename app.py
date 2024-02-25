from flask import Flask, render_template, request, redirect, flash, session
from flask import render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Database"
mongo = PyMongo(app)
users = mongo.db.users
app.config["SECRET_KEY"] = "kjsdfjsdjfsdfosfpsoifjsodfosjfosdfosjfsf"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        print(name, password)
        user = users.find_one({"name": name})
        if user:
            if user.get("password") == password:
                session["user"] = name
                return redirect("/internship")
            else:
                flash("Wrong Password! Please try again.")
                return redirect(request.url)
        else:
            flash("User Does not exist !!")
            return redirect(request.url)
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if name and email and phone and password and password == confirm_password:
            users.insert_one(
                {"name": name, "phone": phone, "email": email, "password": password}
            )
            flash("Successfully signed up")
            return redirect("/internship")
        else:
            flash("Failed to sign up")
            return render_template("signup.html")
    return render_template("signup.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/internship")
def internship():
    return render_template("internship.html")


@app.route("/apply")
def apply():
    return render_template("apply.html")


if __name__ == "__main__":
    app.run(debug=True)
