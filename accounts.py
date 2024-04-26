from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import render_template, session
import secrets


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
            try:
                sql = text("INSERT INTO Accounts (username, password, rights) VALUES (:username, :password, :rights)")
                db.session.execute(sql, {"username": username, "password": hash_value, "rights": rights})
                db.session.commit()
                return True #redirect("/login")

            except:
                return render_template("error.html", message=error_message + "Käyttäjänimi on jo olemassa!")
    
def check_username(username):
    sql = text("SELECT id, password FROM Accounts WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def login(username, password):
    user = check_username(username)  
    
    if not user:
        return render_template("error.html", message=error_message + "Et ole vielä käyttäjä!")
        
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return render_template("error.html", message="käyttäjänimi ja salasana eivät täsmää")

def check_rights():
    if session:
        username = session["username"]
        sql = text("SELECT rights FROM Accounts WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        
        if user.rights == 'admin':
            return True
        else:
            return False
    if not session:
        return False


def check_changes(change, username):
    user = check_username(username)
    if not user:
        return False
    
    if change == "admin":
        return update_rights(username)
    if change == "visitor":
        return change_to_visitor(username)
    if change == "delete":
        return delete_account(username)

def update_rights(username):
    try:
        sql = text("UPDATE Accounts SET rights='admin' WHERE username=:username")
        db.session.execute(sql, {"username":username})
        db.session.commit()
        return True
    except:
        return False
    
def change_to_visitor(username):
    user = check_username(username)
    if not user:
        return False
    try:
        sql = text("UPDATE Accounts SET rights='visitor' WHERE username=:username")
        db.session.execute(sql, {"username":username})
        db.session.commit()
        return True
    except:
        return False

def delete_account(username):
    try:
        sql = text("DELETE FROM Accounts WHERE username=:username")
        db.session.execute(sql, {"username":username})
        db.session.commit()
        return True
    except:
        return False
    
