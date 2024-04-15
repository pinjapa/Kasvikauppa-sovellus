from db import db
from sqlalchemy.sql import text

def add_message(username, content):
    sql = text("INSERT INTO Messages (username, content) VALUES (:username, :content)")
    db.session.execute(sql, {"username": username, "content": content})
    db.session.commit()


def get_messages(): 
    result = db.session.execute(text("SELECT username, content FROM Messages"))
    all_messages = result.fetchall()
    return all_messages