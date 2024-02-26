from flask import Flask, render_template, request, redirect, flash, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Database"
mongo = PyMongo(app)
users = mongo.db.users
app.config["SECRET_KEY"] = "kjsdfjsdjfsdfosfpsoifjsodfosjfosdfosjfsf"

bcrypt = Bcrypt(app)


@app.route("/", methods=["GET", "POST"])
def home():
    if "user" in session:
        return render_template("internship.html")

    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        user = users.find_one({"name": name})
        if user:
            if bcrypt.check_password_hash(user.get("password"), password):
                session["user"] = name
                flash("  Success alert! You have Logged in successfully")
                return render_template("internship.html")
            else:
                flash("  Wrong Password! Please try again.  ")
                return redirect(request.url)
        else:
            flash("  User Does not exist !!  ")
            return redirect(request.url)

    else:
        return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if name and email and phone and password and password and confirm_password:
            if password == confirm_password:
                hpassword = bcrypt.generate_password_hash(password).decode("utf-8")
                users.insert_one(
                    {
                        "name": name,
                        "phone": phone,
                        "email": email,
                        "password": hpassword,
                    }
                )
                flash("   Success alert! You have Signed UP successfully ")
                return render_template("internship.html")
            else:
                flash("Password does not match !!")
                return render_template(request.url)

        else:
            flash("All Fields are required")
            return render_template(request.url)
    return render_template("signup.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/apply")
def apply():
    return render_template("apply.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("  Info alert! You have Logged Out Successfully  ")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
