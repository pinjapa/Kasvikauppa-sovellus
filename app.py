from flask import Flask
from flask import redirect, render_template, request # url_for
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    words = ["kukat", "köynöskasvit", "kaktukset"]
    return render_template("index.html", message="Tervetuloa!", items=words)

@app.route("/messages")
def index_messages():
    result = db.session.execute(text("SELECT content FROM messages"))
    messages = result.fetchall()
    return render_template("index_messages.html", count=len(messages), messages=messages)

@app.route("/new_message")
def new():
    return render_template("new_message.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = text("INSERT INTO messages (content) VALUES (:content)")
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/messages")

@app.route("/all-plants")
def all_plants():
    result = db.session.execute(text("SELECT name, price FROM plants"))
    plants = result.fetchall()
    return render_template("all_plants.html", count=len(plants), plants=plants)

