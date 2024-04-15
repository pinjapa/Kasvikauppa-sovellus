from app import app
from flask import redirect, render_template, request, session
from sqlalchemy.sql import text
from os import getenv
import messages
import accounts
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
    username = session["username"]
    if len(content) > 500:
        return render_template("error.html", message=error_message + "Palutteesi on liian pitkä!")
    messages.add_message(username, content)
    return redirect("/messages")




@app.route("/login_page")
def login_page():
    return render_template("login_page.html")

@app.route("/create-account-page")
def create_account_page():
    return render_template("create_account.html")

@app.route("/create-account", methods=["POST"]) #creates an account
def create_account(): 
    
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    accounts.create_account(username, password1, password2)
    
    return redirect("/")

@app.route("/login", methods=["POST"]) #login
def login():

    username = request.form["username"]
    password = request.form["password"]
    result = accounts.login(username, password)     
    
    return result

@app.route("/logout") 
def logout():
    del session["username"]
    return redirect("/")




@app.route("/all-plants") #page where you can see plants
def all_plants():
    result = db.session.execute(text("SELECT name, price FROM Plants"))
    plants = result.fetchall()
    
    #username = session["username"]
    #sql = text("SELECT rights FROM Accounts WHERE username=:username")
    #result = db.session.execute(sql, {"username":username})
    #rights = result.fetchone()   

    return render_template("all_plants.html", count=len(plants), plants=plants)


