from app import app
from flask import redirect, render_template, request, session, abort, flash
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
    if "csrf_token" not in session:
        abort(403)
    return render_template("new_message.html")

@app.route("/send", methods=["POST"]) 
def send():                 #adds feeback to the table
    if "csrf_token" not in session:
        abort(403)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    content = request.form["content"]
    username = session["username"]
    if len(content) > 500:
        return render_template("error.html", message=error_message + "Palutteesi on liian pitkä!")
    
    messages.add_message(username, content)
    flash("Palaute lisätty")
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
    result = accounts.create_account(username, password1, password2)
    if result == True:
        flash("Käyttäjän luonti onnistui!")
        return redirect("/login_page")
    else:
        return result

@app.route("/login", methods=["POST"]) #login
def login():

    username = request.form["username"]
    password = request.form["password"]
    result = accounts.login(username, password)
    if result == True:
        flash("Kirjautuminen onnistui!")     
        return redirect("/")
    else:
        return result

@app.route("/logout") 
def logout():
    del session["username"]
    del session["csrf_token"]
    flash("Uloskirjautuminen onnistui!")
    return redirect("/")




@app.route("/all-plants") #page where you can see plants
def all_plants():
    result = db.session.execute(text("SELECT id, name, price FROM Plants"))
    plants = result.fetchall()
    
    if session:
        username = session["username"]
        sql = text("SELECT rights FROM Accounts WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        
        if user.rights == 'admin':
            rights = True
        else:
            rights = False
    if not session:
        rights = False
    
    categories = db.session.execute(text("SELECT * FROM Categories"))

    return render_template("all_plants.html", count=len(plants), plants=plants, rights=rights, categories=categories)

@app.route("/new_plant") #page to create new plant
def new_plant():
    categories = db.session.execute(text("SELECT * FROM Categories"))    
    return render_template("new_plant.html", categories=categories)

@app.route("/save-plant", methods=["POST"]) #saves the plant to databse
def save_plant():
    if "csrf_token" not in session:
        abort(403)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    plant_name = request.form["name"]
    plant_category = request.form["category"]
    plant_price = int(request.form["price"])
    plant_description = request.form["description"]
    username = session["username"]

    result = db.session.execute(text("SELECT id FROM Accounts WHERE username=:username"), {"username" :username})
    username_id = int(result.fetchone()[0])
    
    
    sql = text("INSERT INTO Plants (name, price, category_id ) VALUES (:name, :price, :category_id)")
    db.session.execute(sql, {"name": plant_name, "price": plant_price, "category_id": plant_category})
    db.session.commit()
    
    result = db.session.execute(text("SELECT id FROM Plants WHERE name=:name"), {"name" :plant_name})
    plant_id = int(result.fetchone()[0])

    sql = text("INSERT INTO Descriptions (content, plant_id, username_id) VALUES (:content, :plant_id, :username_id)")
    db.session.execute(sql, {"content": plant_description, "plant_id": plant_id, "username_id": username_id} )
    db.session.commit()

    flash("Kasvin lisäys onnistui!")
    return redirect("/all-plants")

@app.route("/plant_page/<int:id>")
def plant_page(id):
    sql = text("""SELECT P.name, A.username, P.price, D.content, C.name 
               FROM Descriptions D, Plants P, Accounts A, Categories C 
               WHERE D.plant_id = P.id
               AND D.username_id = A.id
               AND P.category_id = C.id
               AND D.id=:id
               ;""")
    result = db.session.execute(sql, {"id":id})
    all = result.fetchone()
    name = all[0]
    username = all[1]
    price= all[2]
    content = all[3]
    category = all[4]
    return render_template("plant_page.html",name=name, username=username, price=price, content=content, category=category)
