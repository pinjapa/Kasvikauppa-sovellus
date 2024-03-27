from flask import Flask
from flask import redirect, render_template, request, session # url_for
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")         #front page
def index():
    words = ["kukat", "köynöskasvit", "kaktukset"]
    return render_template("index.html", message="Tervetuloa!", items=words)

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

#@app.route("/result", methods=["POST"])
#def result():
    return render_template("result.html", username=request.form["username"])


@app.route("/logout") 
def logout():
    del session["username"]
    return redirect("/")

@app.route("/messages") #feedback page
def index_messages():
    result = db.session.execute(text("SELECT content FROM messages"))
    messages = result.fetchall()
    return render_template("index_messages.html", count=len(messages), messages=messages)

@app.route("/new_message") #page for new message
def new():
    return render_template("new_message.html")

@app.route("/send", methods=["POST"]) 
def send():                 #adds feeback to the table
    content = request.form["content"]
    sql = text("INSERT INTO messages (content) VALUES (:content)")
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/messages")

@app.route("/all-plants") #page where you can see plants
def all_plants():
    result = db.session.execute(text("SELECT name, price FROM plants"))
    plants = result.fetchall()
    return render_template("all_plants.html", count=len(plants), plants=plants)



