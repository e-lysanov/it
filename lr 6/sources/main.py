import psycopg2
import telebot
import datetime
import utils
import models
import config
import configurate_db

configurate_db.configure()
connection = psycopg2.connect(
    host=config.host,
    user=config.user,
    password=config.password,
    database=config.db_name
)
connection.autocommit = True

token = '5000245694:AAFX6lTh79JaJMuw1QGX4uVnb9C1oKcJgHQ'
bot = telebot.TeleBot(token)
DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]


@bot.message_handler(content_types='text')
def set_response(message):
    is_even = utils.is_week_even(datetime.datetime.now())
    if message.text.strip() == "/start":
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Расписание на текущую неделю",
                     "Расписание на следующую неделю")
        bot.send_message(message.chat.id, 'Выберите, что вам нужно', reply_markup= keyboard)
    elif message.text.strip() == "/week":
        if (utils.is_week_even(datetime.datetime.now())) % 2 != 0:
            bot.send_message(message.chat.id, f'Верхняя')
        else:
            bot.send_message(message.chat.id, f'Нижняя')
    elif message.text.strip() == "/mtuci":
        bot.send_message(message.chat.id, "Тогда Вам сюда: https://mtuci.ru")
    elif message.text.strip() == "/help":
        bot.send_message(message.chat.id, 'Я умею:\n'
                                          '/start - для вывода экранной клавиатуры.\n'
                                          '/mtuci - для получения ссылки на сайт университета.\n'
                                          '/week - узнать четность недели.\n'
                                          'Также я умею выводить расписание - для этого воспользуйтесь экранной клавиатурой!')
    elif message.text.strip() in DAYS:
        day_msg = message.text.strip()
        schedule = models.DaySchedule.get_day_schedule_by_day_name(day_msg, is_even, connection).represent(connection)
        bot.send_message(message.chat.id, schedule)
    elif message.text.strip() == "Расписание на текущую неделю":
        result = ""
        for day in DAYS:
            result += models.DaySchedule.get_day_schedule_by_day_name(day,
                                                                      is_even,
                                                                      connection).represent(connection) + "\n"
        bot.send_message(message.chat.id, result)
    elif message.text.strip() == "Расписание на следующую неделю":
        next_week = datetime.datetime.now() + datetime.timedelta(days=7)
        is_even = utils.is_week_even(next_week)
        result = ""
        for day in DAYS:
            result += models.DaySchedule.get_day_schedule_by_day_name(day,
                                                                      is_even,
                                                                      connection).represent(connection) + "\n"
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, "Я Вас не понял:( Напишите /help")


bot.infinity_polling()
