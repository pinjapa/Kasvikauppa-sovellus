from db import db
from sqlalchemy.sql import text

def add_message(username, content, stars):
    sql = text("""INSERT INTO Feedbacks (username, content, stars)
                VALUES (:username, :content, :stars)""")
    db.session.execute(sql, {"username": username, "content": content, "stars": stars})
    db.session.commit()

def get_average():
    result = db.session.execute(text("SELECT ROUND(AVG(stars),1) FROM Feedbacks"))
    avg = result.fetchone()[0]
    return avg

def get_messages(): 
    result = db.session.execute(text("""SELECT COUNT(id), username, content, AVG(stars)
                                      FROM Feedbacks 
                                     GROUP BY username, content"""))
    all_messages = result.fetchall()
    return all_messages

def delete_message(content):
    sql = (text("""DELETE FROM Feedbacks WHERE content=:content"""))
    db.session.execute(sql, {"content": content})
    db.session.commit()