from db import db
from sqlalchemy.sql import text

def fetch_plants():
    result = db.session.execute(text("SELECT id, name, price FROM Plants"))
    plants = result.fetchall()

    categories = db.session.execute(text("SELECT * FROM Categories"))
    
    sql = db.session.execute(text("SELECT COUNT(id) FROM Plants"))
    sum = sql.fetchone()[0]
    
    return (plants, categories, sum)

def save_plant(plant_name, plant_category, plant_price, plant_description, username):
    try:
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
        return True
    
    except:
        return False

def plantpage(id):
    sql = text("""SELECT P.name, A.username, P.price, D.content, C.name 
               FROM Descriptions D JOIN Plants P ON D.plant_id = P.id
                                   JOIN Accounts A ON D.username_id = A.id
                                   JOIN Categories C ON P.category_id = C.id
               WHERE D.id=:id
               ;""")
    result = db.session.execute(sql, {"id":id})
    all = result.fetchone()
   
    return all

def filter_by_category(category):
    if category == "all":
        sql = text("""SELECT P.id, P.name, P.price
                    FROM Plants P, Categories C
                    WHERE P.category_id = C.id""")
        result = db.session.execute(sql, {"category":category})
        all = result.fetchall()
        return all
    
    elif category == "lowest":
        sql = text("""SELECT P.id, P.name, P.price
                    FROM Plants P, Categories C
                    WHERE P.category_id = C.id
                    ORDER BY P.price""")
        result = db.session.execute(sql, {"category":category})
        all = result.fetchall()
        return all
    
    elif category == "highest":
        sql = text("""SELECT P.id, P.name, P.price
                    FROM Plants P, Categories C
                    WHERE P.category_id = C.id
                    ORDER BY P.price DESC""")
        result = db.session.execute(sql, {"category":category})
        all = result.fetchall()
        return all
    
    else:
        sql = text("""SELECT P.id, P.name, P.price
                    FROM Plants P, Categories C
                    WHERE P.category_id = C.id
                    AND C.id=:category""")
        result = db.session.execute(sql, {"category":category})
        all = result.fetchall()
    
        return all
        