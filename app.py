import telebot
from config import TOKEN, currencies
from extensions import APIException, Converting


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def beginning(message: telebot.types.Message):
    text = "Для правильной конвертации валюты отправьте сообщение в виде:" \
           "\n<имя валюты, цену которой Вы хотите узнать>" \
           " <имя валюты, в которой надо узнать цену первой валюты>" \
           " <количество первой валюты>." \
           "\nВводить буквы необходимо на кириллице, " \
           "без орфографических ошибок!" \
           "\nСписок доступных валют: /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def currency(message: telebot.types.Message):
    text = ""
    for key in currencies:
        text += f"\n{key}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def action(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        for i in range(3):
            values[i] = values[i].lower()
        Converting.checking(values)
        base, quote, amount = values
        text = Converting.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя: \n{e}")
    except Exception:
        bot.reply_to(message, "Ошибка сервера!")
    else:
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
