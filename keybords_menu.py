from telebot import types

cancel1 = types.InlineKeyboardButton(text='⬅', callback_data='cancel1')
cancel2 = types.InlineKeyboardButton(text='⬅', callback_data='cancel2')
ready = types.InlineKeyboardButton(text='Готово!', callback_data='Готово')

# главная клавиатура, вызывается при команде order_sushi
main_keyboard = types.InlineKeyboardMarkup()
main_keyboard.add(types.InlineKeyboardButton(text='Готовый сет', callback_data='r_set'))
main_keyboard.add(types.InlineKeyboardButton(text='Быстрый сет', callback_data='f_set'))
main_keyboard.add(types.InlineKeyboardButton(text='Свой сет', callback_data='m_set'))

# клавиатура наборов
r_set_keyboard = types.InlineKeyboardMarkup()
r_set_keyboard.add(types.InlineKeyboardButton(text='Фидель', callback_data='Фидель'))
r_set_keyboard.add(types.InlineKeyboardButton(text='Бумеранг', callback_data='Бумеранг'))
r_set_keyboard.add(ready)
r_set_keyboard.add(cancel1)

# клавиатура быстрых наборов
f_set_keyboard = types.InlineKeyboardMarkup()
f_set_keyboard.add(types.InlineKeyboardButton(text='Филадельфия', callback_data='Филадельфия'))
f_set_keyboard.add(types.InlineKeyboardButton(text='Суши Лосось', callback_data='Суши Лосось'))
f_set_keyboard.add(types.InlineKeyboardButton(text='Катана', callback_data='Катана'))
f_set_keyboard.add(types.InlineKeyboardButton(text='Атлантика', callback_data='Атлантика'))
f_set_keyboard.add(ready)
f_set_keyboard.add(cancel1)

# клавиатура быстрых наборов
m_set_keyboard = types.InlineKeyboardMarkup()
m_set_keyboard.add(types.InlineKeyboardButton(text='Филадельфия', callback_data='Филадельфия'))
m_set_keyboard.add(types.InlineKeyboardButton(text='Суши Лосось', callback_data='Суши Лосось'))
m_set_keyboard.add(types.InlineKeyboardButton(text='Катана', callback_data='Катана'))
m_set_keyboard.add(types.InlineKeyboardButton(text='Атлантика', callback_data='Атлантика'))
m_set_keyboard.add(ready)
m_set_keyboard.add(cancel1)


# клавиатура заказа
order_keyboard = types.InlineKeyboardMarkup()
order_keyboard.add(types.InlineKeyboardButton(text='Заказать', callback_data='order'))
order_keyboard.add(cancel2)

