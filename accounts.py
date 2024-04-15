from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template, redirect, session

error_message = "Tapahtui virhe: "

def create_account(username, password1, password2):
    rights = "visitor"

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
            sql = text("INSERT INTO Accounts (username, password, rights) VALUES (:username, :password, :rights)")
            db.session.execute(sql, {"username": username, "password": hash_value, "rights": rights})
            db.session.commit()
    

def login(username, password):
    
    sql = text("SELECT id, password FROM Accounts WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()  
    
    if not user:
        return render_template("error.html", message=error_message + "Et ole vielä käyttäjä!")
        
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html", message="käyttäjänimi ja salasana eivät täsmää")