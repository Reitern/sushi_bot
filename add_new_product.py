import sqlite3


db = sqlite3.connect('sushi.db', check_same_thread=False)
cursor = db.cursor()

print("loading...")

sets = ["Фидель", "Бумеранг"]
sushis = ["Филадельфия", "Суши Лосось", "Катана", "Атлантика"]

product_name = sets[0]
count_plus = 5

cursor.execute(f"""UPDATE products SET count_p = 
                (SELECT count_p FROM products WHERE product_name = ?) + ?
                WHERE product_name = ?""", (product_name, count_plus, product_name))

db.commit()
