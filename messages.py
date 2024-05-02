from db import db
from sqlalchemy.sql import text

def add_message(username, content):
    sql = text("""INSERT INTO Feedbacks (username, content)
                VALUES (:username, :content)""")
    db.session.execute(sql, {"username": username, "content": content})
    db.session.commit()

def add_rating(stars):
    sql = text("""INSERT INTO Ratings (stars)
                VALUES (:stars)""")
    db.session.execute(sql, {"stars": stars})
    db.session.commit()

def get_average():
    result = db.session.execute(text("SELECT ROUND(AVG(stars),1) FROM Ratings"))
    avg = result.fetchone()[0]
    return avg

def get_messages(): 
    result = db.session.execute(text("""SELECT COUNT(id), username, content
                                      FROM Feedbacks 
                                     GROUP BY username, content"""))
    all_messages = result.fetchall()
    return all_messages

def delete_message(content):
    sql = (text("""DELETE FROM Feedbacks WHERE content=:content"""))
    db.session.execute(sql, {"content": content})
    db.session.commit()