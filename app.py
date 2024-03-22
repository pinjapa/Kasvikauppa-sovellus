from flask import Flask
from flask import redirect, render_template, request, url_for
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"
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

