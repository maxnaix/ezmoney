import time
import threading
import os
import queue  

import telebot

import binanced as b


bdUsers = {}
path_bd = "data/users/"
mtx = threading.Lock()
start_time = time.time()
hostQueue = queue.Queue() 
t = b.BinanceThread(hostQueue)


def bd_load():
	global bdUsers
	files = os.listdir(path_bd)
	for f in files:
		with open(path_bd+f) as file:
			chat_id = file.readline()
		if chat_id == "":
			bdUsers[f] = None
		else:
			bdUsers[f] = int(chat_id)


def bd_update(name, chat_id):
	global bdUsers
	if chat_id is not None:	
		bdUsers[name] = chat_id
		with open(path_bd+name, 'w') as file:
			f = file.writelines(str(chat_id))
	else:
		bdUsers[name] = None
		with open(path_bd+name, 'w') as file:
			pass			


def bd_name_is_en(name):
	global bdUsers
	if name in bdUsers:
		return True
	return False


def bd_name_is_reg(name):
	global bdUsers
	if bd_name_is_en(name):
		if bdUsers[name] is not None:
			return True
	return False		


def telegram_handler():
	global t
	t.setDaemon(True)
	t.start()

	bd_load()
	with open("data/telegram.txt") as file: 
		token = file.readline()
	bot = telebot.TeleBot(token)

#################################################################################
	@bot.message_handler(commands=['start'])
	def send_start(message):
		global mtx
		with mtx:
			if bd_name_is_en(message.from_user.username):
				bd_update(message.from_user.username, message.from_user.id)
				bot.send_message(message.from_user.id, "start - ok, /help - для справки")


	@bot.message_handler(commands=['help'])
	def send_help(message):
		global mtx
		with mtx:
			if bd_name_is_reg(message.from_user.username):
				s = ('''
/help - справка по командам
/time - время непрерывной работы бота 
/balance - баланс
'''	)
				bot.send_message(message.from_user.id, s)


	@bot.message_handler(commands=['time'])
	def send_time(message):
		global mtx
		global start_time
		with mtx:
			if bd_name_is_reg(message.from_user.username):
				t = int(time.time() - start_time)
				s = "Work time: {0}h {1}m {2}s".format((t // 60) // 60, (t // 60) % 60, t % 60)
				bot.send_message(message.from_user.id, s)


	@bot.message_handler(commands=['balance'])
	def send_balance(message):
		global mtx
		with mtx:
			if bd_name_is_reg(message.from_user.username):
				bot.send_message(message.from_user.id, t.get_balance())


#################################################################################
	threading.Thread(target=bot.infinity_polling, daemon=True).start()
	global mtx
	with mtx:
		for _, chat_id in bdUsers.items():
			if chat_id is not None:
				bot.send_message(chat_id, "start bot, /help - для справки")

	global hostQueue
	while True:
		msg = hostQueue.get()
		with mtx:
			pass
