from telebot import types


def menu():
    markup = types.ReplyKeyboardMarkup()
    buttons = [types.InlineKeyboardButton("Меню", callback_data="menu"),
               types.InlineKeyboardButton("Отправить деньги", callback_data="pay"),
               types.InlineKeyboardButton("Получить деньги", callback_data="get")]

    for button in buttons:
        markup.row(button)

    return markup