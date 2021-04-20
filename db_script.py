import sqlite3


db = sqlite3.connect('sushi.db', check_same_thread=False)
cursor = db.cursor()


def create_tables():
    cursor.execute("""CREATE TABLE IF NOT EXISTS products(
            product_name TEXT PRIMARY KEY,
            composition INT,
            count_p INT);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
                id INT PRIMARY KEY,
                customer TEXT);""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS products_in_order(
                    order_id INT,
                    product_name INT,
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (product_name) REFERENCES products(product_name));""")


# create_tables()

# cursor.execute("""INSERT INTO products VALUES ('Филадельфия', 'Состав: Лосось, Сыр Креметто, Огурец', 20),
#                                               ('Суши Лосось', 'Состав: Лосось, Рис.', 20),
#                                               ('Катана', 'Состав: Пармезан, Кура копченая, Помидор, Пекинка, Сливочный сыр, Кунжут микс, соус цезарь.', 20),
#                                               ('Атлантика', 'Состав: Кура темпура, омлет, ананас консервированный, огурец, соус сладкий чили, кунжут микс.', 20),
#                                               ('Фидель', 'Состав: ролл Филадельфия, ролл Лейла, Запечёный ролл Крабик хот. Количество кусочков: 24', 20),
#                                               ('Бумеранг', 'Состав: ролл Филадельфия с сыром, ролл Филадельфия в масаго, ролл Филадельфия.Количество кусочков: 24 шт.', 20)""")
#
# db.commit()

# сет1 = Фидель; сет 2 = Бумеранг

# for value in cursor.execute("SELECT * FROM products"):
#     print(value)
