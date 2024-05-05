from app import app
from flask import redirect, render_template, request, session, abort, flash
from os import getenv
import messages
import accounts
import plants

app.secret_key = getenv("SECRET_KEY")
error_message = "Tapahtui virhe: "

#front page
@app.route("/")         
def index():
    avg = messages.get_average()
    if not avg:
        avg = "_"
    return render_template("index.html", message="Tervetuloa!", avg=avg)


#feedback page
@app.route("/messages") 
def index_messages():
    all_messages = messages.get_messages()
    rights = accounts.check_rights()
    return render_template("index_messages.html",count=len(all_messages), messages=all_messages, rights=rights)


#removes a message
@app.route("/remove-message", methods=["POST"]) 
def remove_message():
    try:
        content = request.form["remove"]
        messages.delete_message(content)
        flash("Poisto onnistui!", "flash-succeed")
        return redirect("/messages")

    except:
        flash("Poisto epäonnistui!", "flash-error")
        return redirect("/messages")


#page for new message
@app.route("/new_message") 
def new():
    if "csrf_token" not in session:
        abort(403)
    return render_template("new_message.html")


#adds feeback to the table
@app.route("/send", methods=["POST"]) 
def send():                 
    if "csrf_token" not in session:
        abort(403)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    content = request.form["content"]
    username = session["username"]
    if len(content) > 500:
        return render_template("error.html", message=error_message + "Palutteesi on liian pitkä!")
    try:
        messages.add_message(username, content)
        stars = int(request.form["stars"])
        if stars > 0:
            messages.add_rating(stars)
        flash("Palaute lisätty", "flash-succeed")
        return redirect("/messages")
    except:
        flash("Valitse arvio!", "flash-neutral")
        return redirect("/new_message")


#leads to login page
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


#leads to create-account-page
@app.route("/create-account-page")
def create_account_page():
    return render_template("create_account.html")


#creates an account
@app.route("/create-account", methods=["POST"]) 
def create_account(): 
    
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    result = accounts.create_account(username, password1, password2)
    if result == True:
        flash("Käyttäjän luonti onnistui! Olet kirjautuneena sisään", "flash-succeed")
        return redirect("/login_page")
    else:
        flash("Käyttäjän luonti epäonnistui!", "flash-error")
        return redirect("/login_page")


#login function
@app.route("/login", methods=["POST"]) 
def login():

    username = request.form["username"]
    password = request.form["password"]
    result = accounts.login(username, password)
    if result == True:
        flash("Kirjautuminen onnistui!", "flash-succeed")     
        return redirect("/")
    else:
        return result


#logout function
@app.route("/logout") 
def logout():
    del session["username"]
    del session["csrf_token"]
    flash("Uloskirjautuminen onnistui!", "flash-succeed")
    return redirect("/")


#updates users rights
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
        flash("Valitse muutos ensin!", "flash-neutral")
        return redirect("/login_page")
    
    result = accounts.check_changes(changes, username)

    if result:
        flash("Päivittäminen onnistui!", "flash-succeed")
        return redirect("/login_page")
    else:
        flash("Päivittäminen epäonnistui!", "flash-error")
        return redirect("/login_page")


#page where you can see plants
@app.route("/all-plants-page")
def all_plants_page():
    rights = accounts.check_rights()
    result = plants.fetch_plants()
    return render_template("all_plants.html", count=result[2], plants=result[0], rights=rights, categories=result[1])


#to filter plants
@app.route("/all-plants", methods=["POST"]) 
def all_plants():
    rights = accounts.check_rights()
    try:
        wanted_category = request.form["category"]
        plant_s = plants.filter_by_category(wanted_category)
        categories = plants.fetch_plants()[1]
        return render_template("all_plants.html",count=len(plant_s), plants=plant_s, rights=rights, categories=categories)
    
    except:
        flash("Valitse kategoria tai hinta ensin!", "flash-neutral")
        return redirect("/all-plants-page")     


#page to create new plant
@app.route("/new_plant") 
def new_plant():
    if "csrf_token" not in session:
        abort(403)
    categories = plants.fetch_plants()[1]    
    return render_template("new_plant.html", categories=categories)


#saves the plant to database
@app.route("/save-plant", methods=["POST"]) 
def save_plant():
    if "csrf_token" not in session:
        abort(403)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    plant_name = request.form["name"]
    plant_category = request.form["category"]
    try:
        plant_price = int(request.form["price"])
    except:
        flash("Tarkista hinta!", "flash-neutral")
        return redirect("/new_plant")
    plant_description = request.form["description"]
    username = session["username"]

    result = plants.save_plant(plant_name, plant_category, plant_price, plant_description, username)
    if result:
        flash("Kasvin lisäys onnistui!", "flash-succeed")
    else:
        flash("Kasvin lisääminen epäonnistui!", "flash-error")
    return redirect("/all-plants-page")


#page for individual plant
@app.route("/plant_page/<int:id>") 
def plant_page(id):
    result = plants.plantpage(id)
    
    return render_template("plant_page.html",name=result[0], username=result[1], price=result[2], content=result[3], category=result[4])
