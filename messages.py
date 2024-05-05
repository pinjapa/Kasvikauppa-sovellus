from db import db
from sqlalchemy.sql import text


#add feedback/message to database
def add_message(username, content):
    sql = text("""INSERT INTO Feedbacks (username, content)
                VALUES (:username, :content)""")
    db.session.execute(sql, {"username": username, "content": content})
    db.session.commit()


#add star rating to database
def add_rating(stars):
    sql = text("""INSERT INTO Ratings (stars)
                VALUES (:stars)""")
    db.session.execute(sql, {"stars": stars})
    db.session.commit()


#counts average stars
def get_average():
    result = db.session.execute(text("SELECT ROUND(AVG(stars),1) FROM Ratings"))
    avg = result.fetchone()[0]
    return avg


#gets all messages in database
def get_messages(): 
    result = db.session.execute(text("""SELECT COUNT(id), username, content
                                      FROM Feedbacks 
                                     GROUP BY username, content"""))
    all_messages = result.fetchall()
    return all_messages


#deletes a message from database
def delete_message(content):
    sql = (text("""DELETE FROM Feedbacks WHERE content=:content"""))
    db.session.execute(sql, {"content": content})
    db.session.commit()