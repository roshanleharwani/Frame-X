from flask import Flask, render_template, request, redirect, flash, session, url_for
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import os
import json
import secrets

with open("config.json") as file:
    data = json.load(file)
    params = data["params"]


app = Flask(__name__)
uri = "mongodb+srv://roshanleharwani:kYBdCTFNi3u6ktif@users.lo1ne1j.mongodb.net/?retryWrites=true&w=majority&appName=Users"
client = MongoClient(uri)
db = client.users


app.config["SECRET_KEY"] = "kjsdfjsdjfsdfosfpsoifjsodfosjfosdfosjfsf"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = params["email"]
app.config["MAIL_PASSWORD"] = params["pass"]
app.config["MAIL_DEFAULT_SENDER"] = params["email"]

mail = Mail(app)

bcrypt = Bcrypt(app)


def generate_token():
    return secrets.token_hex(16)


@app.route("/", methods=["GET", "POST"])
def home():
    if "user" in session:
        return render_template("internship.html")

    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        user = db.users.find_one({"name": name})
        if user:
            if bcrypt.check_password_hash(user.get("password"), password):
                session["user"] = name
                flash("Success alert! You have Logged in successfully")
                return render_template("internship.html")
            else:
                flash("Invalid Credentials !!  ")
                return redirect(request.url)
        else:
            flash("User Does not exist !!  ")
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
                db.users.insert_one(
                    {
                        "name": name,
                        "phone": phone,
                        "email": email,
                        "password": hpassword,
                    }
                )
                flash("Success alert! You have Signed UP successfully ")
                session["user"] = name
                return render_template("internship.html")
            else:
                flash("Password does not match !!")
                return render_template("signup.html")

        else:
            flash("All Fields are required")
            return render_template("signup.html")
    return render_template("signup.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        email = request.form.get("email")
        subject = request.form.get("subject")
        msg = request.form.get("message")
        message = Message(subject=subject, recipients=[params["email"]])
        message.body = f"{msg}\n\nEmail: {email}"
        mail.send(message)
        return render_template("contact.html")
    else:
        return render_template("contact.html")


@app.route("/apply")
def apply():
    if "user" in session:
        return render_template("apply.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Info alert! You have Logged Out Successfully  ")
    return redirect("/")


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = db.users.find_one({"reset_token": token})
    if user:
        if request.method == "POST":
            new_password = request.form["password"]
            # Update user's password and remove the reset token
            db.users.update_one(
                {"reset_token": token},
                {
                    "$set": {
                        "password": bcrypt.generate_password_hash(new_password),
                        "reset_token": None,
                    }
                },
            )
            flash(
                "Your password has been reset successfully. You can now login with your new password."
            )
            return redirect("/")
        return render_template("reset_password_request.html", token=token)
    else:
        flash("Invalid or expired reset token.")
        return redirect(url_for("home"))


@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if request.method == "POST":
        email = request.form["email"]
        user = db.users.find_one({"email": email})
        if user:
            reset_token = generate_token()
            # Store reset_token in the database with the user's email
            db.users.update_one(
                {"email": email}, {"$set": {"reset_token": reset_token}}
            )
            # Send email with reset link
            reset_link = url_for("reset_password", token=reset_token, _external=True)
            msg = Message("Password Reset Request", recipients=[email])
            msg.body = f"Click the following link to reset your password: {reset_link}"
            mail.send(msg)
            flash(
                "An email with instructions to reset your password has been sent to your email address."
            )
            return redirect(url_for("home"))
        else:
            flash("No user found with that email address.")
    return render_template("recover.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if "user" not in session:
        return redirect(request.url)
    else:
        redirect(request.url)

    if request.method == "POST":
        file = request.files["resume"]
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            db.users.insert_one({"filename": filename, "name": session["user"]})
            flash("File uploaded Successfully")
            return redirect(request.url)
    return "Upload file"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9999)
