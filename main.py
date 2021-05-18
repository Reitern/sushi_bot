from db_script import *
from keybords_menu import *
import telebot
from config import TOKEN, OWNER_ID


is_running = running1 = False
main_menu = ''
main_data = ''
main_number = ''
order_id = 0

bot = telebot.TeleBot(TOKEN)

create_tables()
db.commit()


def main_order(chat_id):
    question = "Что вы хотите заказать?"
    bot.send_message(chat_id, text=question, reply_markup=main_keyboard)


def order(chat_id, data):
    global main_data
    cursor.execute(f"SELECT * FROM products WHERE product_name = ?;", (data, ))
    result = cursor.fetchone()
    print(result)
    main_data = data
    path = "./photos/" + data + ".jpg"
    bot.send_photo(chat_id, open(path, 'rb'))
    text = "*Наименование:* " + result[0] + "\n" + "*Состав:* " + result[1]
    if not main_menu == "m_set":
        text = text + "\n" + "*Количество в наличии:* " + str(result[2])
    bot.send_message(chat_id, text, parse_mode="Markdown")
    bot.send_message(chat_id, text='Заказать?', reply_markup=order_keyboard)


def r_set(chat_id):
    question = "Выберите наборы"
    bot.send_message(chat_id, text=question, reply_markup=r_set_keyboard)


def f_set(chat_id):
    question = "Выберите суши из наличия"
    bot.send_message(chat_id, text=question, reply_markup=f_set_keyboard)


def m_set(chat_id):
    question = "Выберите суши"
    bot.send_message(chat_id, text=question, reply_markup=m_set_keyboard)


def rec(message):
    bot.send_message(message.chat.id, "Записали")
    if main_menu == "r_set":
        r_set(message.chat.id)
    elif main_menu == "f_set":
        f_set(message.chat.id)
    elif main_menu == "m_set":
        m_set(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Error")


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет, {}".format(message.from_user.first_name))


@bot.message_handler(commands=['ordersushi'])
def order_sushi_command(message):
    global is_running, order_id
    cursor.execute(f"""DELETE FROM products_in_order WHERE order_id = 
                    (SELECT id FROM orders WHERE customer = ?);""", (message.from_user.first_name,))
    cursor.execute(f"DELETE FROM orders WHERE customer = ?;", (message.from_user.first_name,))
    db.commit()
    cursor.execute(f"INSERT INTO orders (customer) VALUES (?);", (message.from_user.first_name,))
    cursor.execute(f"SELECT id FROM orders WHERE customer = ?;", (message.from_user.first_name,))
    res = cursor.fetchone()
    order_id = res[0]
    if not is_running:
        main_order(message.chat.id)
        is_running = True


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Привет")
    elif message.text.lower() == "order":
        print("order")
        for value in cursor.execute("SELECT * FROM orders;"):
            print(value)
        print()
        for value in cursor.execute("SELECT * FROM products_in_order;"):
            print(value)
        print()


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global is_running, main_menu, main_number

    if call.data == "r_set":
        r_set(call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        main_menu = call.data
    elif call.data == "f_set":
        f_set(call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        main_menu = call.data
    elif call.data == "m_set":
        m_set(call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        main_menu = call.data
    elif call.data == "cancel1":
        main_order(call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "cancel2":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Ищем дальше")
        if main_menu == "r_set":
            r_set(call.message.chat.id)
        elif main_menu == "f_set":
            f_set(call.message.chat.id)
        elif main_menu == "m_set":
            m_set(call.message.chat.id)
        else:
            bot.send_message(call.message.chat.id, "Error")
    elif call.data == "main_cancel":
        db.rollback()
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Заказ отменён")
        print("main_cancel")
        for value in cursor.execute("SELECT * FROM orders;"):
            print(value)
        print()
        is_running = False
    elif call.data == "Готово":
        cursor.execute(f"""SELECT 1 FROM products_in_order WHERE order_id = ?;""", (order_id,))
        result = cursor.fetchone()
        print(result)
        if result != None:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            msg = bot.send_message(call.message.chat.id, "Введите свой номер телефона")
            bot.register_next_step_handler(msg, ask_number)
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "Вы не выбрали ни одного продукта. Заказ отменён")
        is_running = False
    elif call.data == "order":
        msg = bot.send_message(call.message.chat.id, "Сколько шт. вы хотите?")
        bot.register_next_step_handler(msg, ask_count)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        order(call.message.chat.id, call.data)
        bot.delete_message(call.message.chat.id, call.message.message_id)


def ask_count(message):
    global main_data
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, "Пожалуйста, введите число!")
        bot.register_next_step_handler(msg, ask_count)
    else:
        if main_menu == "m_set":
            if int(message.text) >= 100:
                text = "Мы столько не приготовим :с" + "\n" + "Введите число поменьше"
                msg = bot.send_message(message.chat.id, text)
                bot.register_next_step_handler(msg, ask_count)
            else:
                cursor.execute(f"SELECT id FROM orders WHERE customer = ?;", (message.from_user.first_name,))
                res = cursor.fetchone()
                res1 = "+" + str(main_data)
                data = (str(res[0]), res1, str(message.text))
                print(data)
                cursor.execute("INSERT INTO products_in_order VALUES (?, ?, ?);", data)
                for value in cursor.execute(f"""SELECT * FROM products_in_order WHERE order_id = 
                                (SELECT id FROM orders WHERE customer = ?);""", (message.from_user.first_name,)):
                    print(value)
                print()
                rec(message)
        else:
            cursor.execute(f"SELECT * FROM products WHERE product_name = ?;", (main_data, ))
            result = cursor.fetchone()
            if int(message.text) <= result[2]:
                cursor.execute(f"SELECT id FROM orders WHERE customer = ?;", (message.from_user.first_name,))
                res = cursor.fetchone()
                data = (str(res[0]), str(main_data), str(message.text))
                print(data)
                cursor.execute("INSERT INTO products_in_order VALUES (?, ?, ?);", data)
                for value in cursor.execute(f"""SELECT * FROM products_in_order WHERE order_id = 
                                (SELECT id FROM orders WHERE customer = ?);""", (message.from_user.first_name,)):
                    print(value)
                print()
                cursor.execute(f"""UPDATE products SET count_p = 
                                (SELECT count_p FROM products WHERE product_name = ?) - ?
                                WHERE product_name = ?""", (main_data, message.text, main_data))
                rec(message)
            else:
                text = "У нас нет столько :с" + "\n" + "Введите число в пределах количества"
                msg = bot.send_message(message.chat.id, text)
                bot.register_next_step_handler(msg, ask_count)


def ask_number(message):
    global main_number, order_id
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, "Пожалуйста, введите число!")
        bot.register_next_step_handler(msg, ask_number)
    else:
        main_number = message.text
        bot.send_message(message.chat.id, "Ваш заказ передан администратору")
        bot.send_message(message.chat.id, f"Когда заказ будет собран, по номеру {main_number} с вами "
                                               f"свяжется курьер для уточнения места доставки")
        db.commit()
        bot.send_message(OWNER_ID, "Кто-то сделал заказ!")
        cursor.execute(f"SELECT customer FROM orders WHERE id = ?;", (order_id,))
        res = cursor.fetchone()
        text = "*Заказчик: *" + str(res[0])
        for value in cursor.execute(f"""SELECT * FROM products_in_order WHERE order_id = ?;""", (order_id,)):
            text += "\n" + "*• *" + str(value[1]) + ", " + str(value[2]) + " шт."
        text += "\n" + "*Номер телефона: *" + str(main_number)
        bot.send_message(OWNER_ID, text, parse_mode="Markdown")
        print("main_order")
        for value in cursor.execute("SELECT * FROM orders;"):
            print(value)
        print()


bot.polling(none_stop=True, interval=0)
