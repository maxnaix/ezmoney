import time
import threading
import queue

import telebot

import binanced
import BDClass


def main():
    start_time = time.time()
    mtx = threading.Lock()
    bd = BDClass.BDClass()
    bd.load()

    hostQueue = queue.Queue()
    t = binanced.BinanceThread(hostQueue)
    t.setDaemon(True)
    t.start()

    with open("data/telegram.txt") as file:
        token = file.readline()
    bot = telebot.TeleBot(token)

#################################################################################

    @bot.message_handler(commands=['start'])
    def send_start(message):
        with mtx:
            if bd.is_enabled(message.from_user.username):
                bd.update(message.from_user.username, message.from_user.id)
                bot.send_message(message.from_user.id,
                                 "start - ok, /help - для справки")

    @bot.message_handler(commands=['help'])
    def send_help(message):
        with mtx:
            if bd.is_registered(message.from_user.username):
                s = ('''
/help - справка по командам
/time - время непрерывной работы бота 
/balance - баланс
''')
                bot.send_message(message.from_user.id, s)

    @bot.message_handler(commands=['time'])
    def send_time(message):
        with mtx:
            if bd.is_registered(message.from_user.username):
                t = int(time.time() - start_time)
                s = "Work time: {0}h {1}m {2}s".format(
                    (t // 60) // 60, (t // 60) % 60, t % 60)
                bot.send_message(message.from_user.id, s)

    @bot.message_handler(commands=['balance'])
    def send_balance(message):
        with mtx:
            if bd.is_registered(message.from_user.username):
                bot.send_message(message.from_user.id, t.get_balance())

#################################################################################
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    with mtx:
        lst = bd.get_all_chats()
        for chat in lst:
            bot.send_message(chat, "start bot, /help - для справки")

    while True:
        msg = hostQueue.get()
        with mtx:
            pass


if __name__ == "__main__":
    main()
