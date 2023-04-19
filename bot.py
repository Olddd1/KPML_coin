import io
import traceback

import qrcode

import telebot
import hashlib

import keyboards
import config
import users
from utils import qr_generate

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    user_hash = hashlib.md5(str(user_id).encode()).hexdigest()

    database = users.DataBase()

    user = database.get_user(user_hash)

    if not user:
        user = database.user_create(user_hash)

    if len(message.text.split()) > 1:
        if "cheque" in message:
            cheque = message.text.split()[1].split("__")[0]
            cheque_data = database.get_cheque(cheque)

            amount = cheque_data[3]

            if amount <= user[1]:
                database.update_cheque(cheque, user_hash)
                database.update_user(user_hash, -amount)
                database.update_user(cheque_data[1], amount)
                bot.send_message("Оплата прошла успешно")
            else:
                bot.send_message("Недостаточно средств")


        else:
            address = message.text.split()[1].split("__")[0]
            # TODO: оплата с запросом цены

    markup = keyboards.menu()
    bot.send_message(user_id, "Приветствую! Выбери нужный пункт в меню!", reply_markup=markup)


@bot.message_handler(func=lambda x: x.text == "Меню", content_types=["text"])
def menu(message):
    user_id = message.chat.id
    user_hash = hashlib.md5(str(user_id).encode()).hexdigest()

    user = users.DataBase().get_user(user_hash)

    message_text = f"Адресс вашего кошелька: `{user_hash}`\n" \
                   f"Ваш баланс: {user[1]} KPML_coin"

    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("Сгенерировать QR код"))
    markup.row(telebot.types.InlineKeyboardButton("Запросить перевод"))
    # markup.row(telebot.types.InlineKeyboardButton("Оплатить"))

    bot.send_message(user_id, message_text, reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(func=lambda x: x.text == "Отправить деньги", content_types=["text"])
def pay(message):
    print(message) # TODO: оплата с вводом адреса и суммы

@bot.message_handler(func=lambda x: x.text == "Получить деньги", content_types=["text"])
def get(message):
    user_id = message.chat.id
    user_hash = hashlib.md5(str(user_id).encode()).hexdigest()

    message_text = f"Адресс вашего кошелька: `{user_hash}`"

    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("Сгенерировать QR код"))
    markup.row(telebot.types.InlineKeyboardButton("Запросить перевод"))
    markup.row(telebot.types.InlineKeyboardButton("Меню"))

    bot.send_message(user_id, message_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda x: x.text == "Сгенерировать QR код", content_types=["text"])
def qr_by_address_generate(message):
    user_id = message.chat.id
    user_hash = hashlib.md5(str(user_id).encode()).hexdigest()

    src = f"https://t.me/KPML_money_test_bot/start={user_hash}__address"
    qr_code = qr_generate(src, f"{user_hash}.png")

    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("Меню"))

    bot.send_photo(user_id, qr_code, "QR код успешно сгенерирован", reply_markup=markup)

@bot.message_handler(func=lambda x: x.text == "Запросить перевод", content_types=["text"])
def qr_query(message):
    user_id = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.InlineKeyboardButton("Меню"))
    msg = bot.send_message(user_id, "Отправьте сумму, на которую хотите получить перевод", reply_markup=markup)
    bot.register_next_step_handler(msg, qr_generate_by_money)

def qr_generate_by_money(message):
    user_id = message.chat.id
    try:
        amount = float(message.text)

        user_hash = hashlib.md5(str(user_id).encode()).hexdigest()

        db = users.DataBase()
        cheque = db.create_cheque(f"Оплата на {amount} рублей", amount, user_hash)

        src = f"https://t.me/KPML_money_test_bot/start={cheque}__cheque"
        qr_code = qr_generate(src, f"{cheque}.png")

        markup = telebot.types.ReplyKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("Меню"))

        bot.send_photo(user_id, qr_code, "QR код на оплату сгенерирован", reply_markup=markup)
    except:
        if message.text == "Меню":
            user_id = message.chat.id
            user_hash = hashlib.md5(str(user_id).encode()).hexdigest()

            user = users.DataBase().get_user(user_hash)

            message_text = f"Адресс вашего кошелька: `{user_hash}`\n" \
                           f"Ваш баланс: {user[1]} KPML_coin"

            markup = telebot.types.ReplyKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton("Сгенерировать QR код"))
            markup.row(telebot.types.InlineKeyboardButton("Запросить перевод"))
            # markup.row(telebot.types.InlineKeyboardButton("Оплатить"))

            bot.send_message(user_id, message_text, reply_markup=markup, parse_mode="Markdown")
        else:
            markup = telebot.types.ReplyKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton("Меню"))
            msg = bot.send_message(user_id, "Отправьте сумму, на которую хотите получить платёж", reply_markup=markup)
            bot.register_next_step_handler(msg, qr_generate_by_money)
