from app import app
from flask import redirect, render_template, request, session, abort, flash
from sqlalchemy.sql import text
from os import getenv
import messages
import accounts
import plants
from db import db

app.secret_key = getenv("SECRET_KEY")
error_message = "Tapahtui virhe: "

@app.route("/")         #front page
def index():
    words = ["kukat", "köynöskasvit", "kaktukset"]
    avg=messages.get_average()
    if not avg:
        avg = "_"
    return render_template("index.html", message="Tervetuloa!", items=words, avg=avg)


@app.route("/messages") #feedback page
def index_messages():
    all_messages = messages.get_messages()
    return render_template("index_messages.html",count=len(all_messages), messages=all_messages)

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
    try:
        stars = int(request.form["stars"])
    except:
        flash("Valitse arvio!")
        redirect("/new_message")
    username = session["username"]
    if len(content) > 500:
        return render_template("error.html", message=error_message + "Palutteesi on liian pitkä!")
    
    messages.add_message(username, content, stars)
    flash("Palaute lisätty")
    return redirect("/messages")




@app.route("/login_page")
def login_page():
    rights = accounts.check_rights()
    if rights:
        b_rights = True
        rights = 'admin'
        
    else:
        b_rights = False
        rights = 'visitor'
    return render_template("login_page.html", rights=rights, boolean_rights=b_rights)
       
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
        flash("Olet kirjautunut sisään!")
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

@app.route("/update", methods=["POST"])
def update_rights():
    if "csrf_token" not in session:
        abort(403)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    username = request.form["username"]
    try:
        changes = request.form["changes"]
    except:
        flash("Valitse muutos ensin!")
        return redirect("/login_page")
    
    result = accounts.check_changes(changes, username)

    if result:
        flash("Päivittäminen onnistui!")
        return redirect("/login_page")
    else:
        flash("Päivittäminen epäonnistui!")
        return redirect("/login_page")


@app.route("/all-plants-page")#page where you can see plants
def all_plants_page():
    rights = accounts.check_rights()
    result = plants.fetch_plants()
    return render_template("all_plants.html", count=result[2], plants=result[0], rights=rights, categories=result[1])

@app.route("/all-plants", methods=["POST"]) #to filter plants
def all_plants():
    rights = accounts.check_rights()
    try:
        wanted_category = request.form["category"]
        plant_s = plants.filter_by_category(wanted_category)
        categories = plants.fetch_plants()[1]
        return render_template("all_plants.html",count=len(plant_s), plants=plant_s, rights=rights, categories=categories)
    
    except:
        flash("Valitse kategoria tai hinta ensin!")
        return redirect("/all-plants-page")   
    

@app.route("/new_plant") #page to create new plant
def new_plant():
    if "csrf_token" not in session:
        abort(403)
    categories = plants.fetch_plants()[1]    
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

    result = plants.save_plant(plant_name, plant_category, plant_price, plant_description, username)
    if result:
        flash("Kasvin lisäys onnistui!")
    else:
        flash("Kasvin lisääminen epäonnistui!")
    return redirect("/all-plants-page")

@app.route("/plant_page/<int:id>") #page for individual plant
def plant_page(id):
    result = plants.plantpage(id)
    
    return render_template("plant_page.html",name=result[0], username=result[1], price=result[2], content=result[3], category=result[4])
