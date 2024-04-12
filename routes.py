from app import app
from flask import redirect, render_template, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
import messages
#import accounts
from db import db

app.secret_key = getenv("SECRET_KEY")
error_message = "Tapahtui virhe: "

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
    if len(content) > 500:
        return render_template("error.html", message=error_message + "Palutteesi on liian pitkä!")
    messages.add_message(content)
    return redirect("/messages")




@app.route("/login_page")
def login_page():
    return render_template("login_page.html")

@app.route("/create-account-page")
def create_account_page():
    return render_template("create_account.html")

@app.route("/create-account", methods=["POST"]) 
def create_account(): 
    rights = "visitor"
    
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    
    #checks the given information
    if len(username) < 6:
        return render_template("error.html", message=error_message + "Käyttäjänimi on liian lyhyt!")
    if len(password1) < 8:
        return render_template("error.html", message=error_message + "Salasana on liian lyhyt!")
    
    if len(username) > 20:
        return render_template("error.html", message=error_message + "Käyttäjänimi on liian pitkä!")
    if len(password1) > 20:
        return render_template("error.html", message=error_message + "Salasana on liian pitkä!")
    
    if password1 != password2:
        return render_template("error.html", message=error_message + "Salasanat eivät täsmää!")



    if len(username) >= 6:
        if password1 == password2:
            hash_value = generate_password_hash(password1)
            sql = text("INSERT INTO accounts (username, password, rights) VALUES (:username, :password, :rights)")
            db.session.execute(sql, {"username": username, "password": hash_value, "rights": rights})
            db.session.commit()
    
    return redirect("/")

@app.route("/login", methods=["POST"]) #login
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = text("SELECT password FROM accounts WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()   
    
    if not user:
        return render_template("error.html", message=error_message + "Et ole vielä käyttäjä!")
        
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
        else:
            return render_template("error.html", message="käyttäjänimi ja salasana eivät täsmää")
        
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