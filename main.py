from db_script import *
from keybords_menu import *
from func import *
import telebot
from config import TOKEN


is_running = running1 = running2 = False
main_menu = ''

bot = telebot.TeleBot(TOKEN)

create_tables()
db.commit()


def main_order(chat_id):
    question = "Что вы хотите заказать?"
    bot.send_message(chat_id, text=question, reply_markup=main_keyboard)


def order(chat_id, data):
    cursor.execute(f"SELECT * FROM products WHERE product_name = '" + data + "'")
    result = cursor.fetchone()
    print(result)
    text = "Наименование: " + result[0] + "\n" + "Состав: " + result[1]
    bot.send_message(chat_id, text)
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


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет, {}".format(message.from_user.first_name))


@bot.message_handler(commands=['ordersushi'])
def order_sushi_command(message):
    global is_running
    if not is_running:
        main_order(message.chat.id)
        is_running = True


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Привет")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global is_running, running1, running2, main_menu

    if call.data == "r_set":
        if not running1:
            r_set(call.message.chat.id)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            main_menu = call.data
            running1 = True
    elif call.data == "f_set":
        if not running1:
            f_set(call.message.chat.id)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            main_menu = call.data
            running1 = True
    elif call.data == "m_set":
        if not running1:
            m_set(call.message.chat.id)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            main_menu = call.data
            running1 = True
    elif call.data == "cancel1":
        main_order(call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        running1 = False
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
    elif call.data == "Готово":
        bot.send_message(call.message.chat.id, "Ваш заказ передан администратору")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        is_running = running1 = running2 = False
    elif call.data == "order":
        msg = bot.send_message(call.message.chat.id, "Сколько штучек вы хотите?")
        bot.register_next_step_handler(msg, ask_count)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        order(call.message.chat.id, call.data)
        bot.delete_message(call.message.chat.id, call.message.message_id)


def ask_count(message):
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, "Пожалуйста, введите число!")
        bot.register_next_step_handler(msg, ask_count)
    else:
        if int(message.text) >= 100:
            msg = bot.send_message(message.chat.id, "Мы столько не приготовим :с")
            bot.register_next_step_handler(msg, ask_count)
        else:
            bot.send_message(message.chat.id, "Записали")
            if main_menu == "r_set":
                r_set(message.chat.id)
            elif main_menu == "f_set":
                f_set(message.chat.id)
            elif main_menu == "m_set":
                m_set(message.chat.id)
            else:
                bot.send_message(message.chat.id, "Error")


bot.polling(none_stop=True, interval=0)
