import telebot
from utils import ConvertException,CurrencyConvertion
from settings import TOKEN,keys
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start","help","commands"])
def echo_start(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду в формате:\n" \
           "<Имя валюты> <Из какой валюты перевести1><Из какой валюты перевести2>...<Количество>" \
           "\n список доступных валют /list"
    bot.reply_to(message,text)

@bot.message_handler(commands=["value", "list"])
def list(message: telebot.types.Message):
    text="Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text,key))+" : "+keys[key]
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        entry=message.text.split(" ")
        parts=entry[0],entry[1:-1],entry[-1]
        base,quote,amount=parts
        total_base=CurrencyConvertion.convert(base,quote,amount)
    except ConvertException as e:
        bot.reply_to(message,f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message,f"Не удалось обработать команду\n{e}")
    else:
        text=total_base
        bot.send_message(message.chat.id, text)

bot.polling()
