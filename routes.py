from app import app
from flask import redirect, render_template, request, session
from sqlalchemy.sql import text
#from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
import messages
from db import db

app.secret_key = getenv("SECRET_KEY")

@app.route("/")         #front page
def index():
    words = ["kukat", "köynöskasvit", "kaktukset"]
    return render_template("index.html", message="Tervetuloa!", items=words)


@app.route("/messages") #feedback page
def index_messages():
    all_messages = messages.get_messages()
    return render_template("index_messages.html", count=len(all_messages), messages=all_messages)

@app.route("/new_message") #page for new message
def new():
    return render_template("new_message.html")

@app.route("/send", methods=["POST"]) 
def send():                 #adds feeback to the table
    content = request.form["content"]
    messages.add_message(content)
    return redirect("/messages")


@app.route("/login_page")
def login_page():
    return render_template("login_page.html")

@app.route("/login", methods=["POST"]) #login
def login():
    username = request.form["username"]
    password = request.form["password"]
    #todo: check username and password
    session["username"] = username
    return redirect("/")


@app.route("/create-account", methods=["POST"])
def create_account():
    username = request.form["username"]
    sql = text("INSERT INTO users (username, password, rights ) VALUES (:username, :password, 'basic')")
    db.session.execute(sql, {"username":username, "password":password})
    db.session.commit()
    return redirect("/")


@app.route("/logout") 
def logout():
    del session["username"]
    return redirect("/")



@app.route("/all-plants") #page where you can see plants
def all_plants():
    result = db.session.execute(text("SELECT name, price FROM plants"))
    plants = result.fetchall()
    return render_template("all_plants.html", count=len(plants), plants=plants)