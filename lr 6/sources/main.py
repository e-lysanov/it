import telebot
from telebot import types
import functions, config

bot = telebot.TeleBot(config.token, parse_mode='MARKDOWN')

@bot.message_handler(commands=['start'])
def handle_start_help(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = config.buttons['start_menu']
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Привет. Я подскажу расписание.', reply_markup=keyboard)

@bot.message_handler(content_types='text')
def message_reply(message):
    dataset = {'day': None, 'odd': None}
    if message.text=="Сегодня":
        bot.send_message(message.chat.id, functions.get_rasp(*functions.now_data()))
    elif message.text=="Завтра":
        bot.send_message(message.chat.id, functions.get_rasp(*functions.now_data(1)))
    elif message.text=="Выбрать день":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = config.buttons['odd_menu']
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, 'Выбери неделю', reply_markup=keyboard)
        m = bot.register_next_step_handler(message, lambda m: select_day(m, dataset))

def select_day(message, dataset):
    if message.text == "Чётная":
        dataset['odd'] = True
    elif message.text == "Нечётная":
        dataset['odd'] = False
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = config.buttons['day_menu']
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Выбери день недели', reply_markup=keyboard)
    m = bot.register_next_step_handler(message, lambda m: return_rasp(m, dataset))

def return_rasp(message, dataset):
    dataset['day'] = config.buttons['day_menu'].index(message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = config.buttons['start_menu']
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, functions.get_rasp(dataset['odd'], dataset['day']), reply_markup=keyboard)

if __name__ == "__main__":
    bot.infinity_polling()
    