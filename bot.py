import config
import telebot
from telebot import types
from db import DbConnector

mydb = DbConnector(host=config.host,user=config.user,passwd=config.passwd,database=config.database)

bot = telebot.TeleBot(config.token)
listenUser = {}


@bot.message_handler(commands=['start'])
def start(message):
    if not (mydb.user_exists(message.from_user.id)):
        mydb.add_user(message.from_user.id, message.from_user.first_name)
        mydb.db.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("List all tasks")
    item2 = types.KeyboardButton("Add Task")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Hi", reply_markup=markup)


@bot.message_handler(commands=['add'])
def addTask(message):
    if not (mydb.user_exists(message.from_user.id)):
        mydb.add_user(message.from_user.id, message.from_user.first_name)
        mydb.db.commit()

    task = message.text[5:]
    mydb.add_task(task, message.from_user.id)
    mydb.db.commit()
    bot.send_message(message.chat.id, "Task '{}' inserted".format(task))
    bot.send_message(message.chat.id, "Use /list command to see all of them")


@bot.callback_query_handler(func=lambda call: True)
def answerinline(call):
    task_name = mydb.pop_task(int(call.data), call.from_user.id)
    mydb.db.commit()

    markup = types.InlineKeyboardMarkup(row_width=1)
    tasks = mydb.list_tasks(call.from_user.id)
    if len(tasks):
        for i, x in enumerate(tasks):
            item = types.InlineKeyboardButton("№{} {}".format(
                i + 1, x[1]), callback_data='{}'.format(i + 1))
            markup.add(item)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Нажми на задание если оно выполнено",
                              reply_markup=markup)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Список пуст",
                              reply_markup=None)


@bot.message_handler(commands=['list'])
def showTasks(message):
    if not (mydb.user_exists(message.from_user.id)):
        mydb.add_user(message.from_user.id, message.from_user.first_name)
        mydb.db.commit()
    tasks = mydb.list_tasks(message.from_user.id)
    messageSend = "Tasks to do:\n"
    for i, x in enumerate(tasks):
        messageSend += ("№{} {}\n".format(i + 1, x[1]))
    bot.send_message(message.chat.id, messageSend)


@bot.message_handler(commands=['del'])
def deleteTask(message):
    count = int(message.text[5:])
    task_name = mydb.pop_task(count, message.from_user.id)
    mydb.db.commit()
    bot.send_message(message.chat.id, "Task '{}' deleted".format(task_name))
    bot.send_message(message.chat.id, "Use /list command to see new list")


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text == "List all tasks":
        markup = types.InlineKeyboardMarkup(row_width=1)
        tasks = mydb.list_tasks(message.from_user.id)
        if len(tasks) == 0:
            bot.send_message(message.chat.id, "Список пуст")
        else:
            for i, x in enumerate(tasks):
                item = types.InlineKeyboardButton("№{} {}".format(
                    i + 1, x[1]), callback_data='{}'.format(i + 1))
                markup.add(item)

            bot.send_message(
                message.chat.id, "Нажми на задание если оно выполнено", reply_markup=markup)

    if listenUser.get(message.from_user.id, False):
        mydb.add_task(message.text, message.from_user.id)
        mydb.db.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("List all tasks")
        item2 = types.KeyboardButton("Add Task")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Task '{}' inserted".format(
            message.text), reply_markup=markup)
        listenUser.update({message.from_user.id: False})
    if message.text == "Add Task":
        bot.send_message(message.chat.id, "Введите задание")
        listenUser.update({message.from_user.id: True})


if __name__ == '__main__':
    bot.infinity_polling()
