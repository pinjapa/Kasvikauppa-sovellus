from db import db
from sqlalchemy.sql import text

def add_message(content):
    sql = text("INSERT INTO messages (content) VALUES (:content)")
    db.session.execute(sql, {"content": content})
    db.session.commit()


def get_messages(): 
    result = db.session.execute(text("SELECT content FROM messages"))
    all_messages = result.fetchall()
    return all_messages