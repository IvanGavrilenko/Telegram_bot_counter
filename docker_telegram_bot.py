import os
import telebot, datetime, time, math, re
from telebot import types
from ultralytics import YOLO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BOT_NAME = '' # Имя для бота. Нужно в том случае, если вы хотите обращаться к боту по имени
bot = telebot.TeleBot(BOT_TOKEN)

TIMEOUT_CONNECTION = 5 # Таймаут переподключения

# Сообщение при старте
START_MESSAGE = """Отправьте мне изображение, и я посчитаю количество рулончиков на фотографии или отправьте мне выражение, а я посчитаю"""
# Сообщение поддержки
HELP_MESSAGE = """Мной пользоваться очень просто. Вы мне отправляете фотографию и я считаю рулончики или вы отправлете выражение, а я вам возвращаю его результат.

***Операторы***:
    + - сложение;
    - - вычитание;
    \* - умножение;
    / - деление;
    \*\* - возведение в степнь.
    
***Функции***:
    cos(x) - косинус x;
    sin(x) - синус x;
    tg(x) - тангенс x;
    fact(x) - факториал x;
    sqrt(x) - квадратный корень х;
    sqr(x) - х в квадрате.

***Логарифмы***:
    log2(x) - логарифм х по основанию 2;
    lg(х) - десятичный логарифм х;
    ln(x) - натуральный логарифм x;
    log(b, х) - логарифм х по основанию b;

***Системы счисления***:
    0bx - перевести двоичное число х в десятичное;
    0ox - перевести восьмиричное число х в десятичное;
    0xx - перевести шестнадцатиричное число х в десятичное;"""

пи = п = p = pi = 3.141592653589793238462643 # число Пи asd 

# Ниже все понятно...
def fact(float_):
    return math.factorial(float_)

def cos(float_):
    return math.cos(float_)

def sin(float_):
    return math.sin(float_)

def tg(float_):
    return math.tan(float_)
    
def tan(float_):
    return math.tan(float_)


def ln(float_):
    return math.log(float_)

def log(base, float_):
    return math.log(float_, base)

def lg(float_):
    return math.log10(float_)

def log2(float_):
    return math.log2(float_)

def exp(float_):
    return math.exp(float_)

# Обработчик сообщений-команд
@bot.message_handler(commands=['start', 'help'])
def send_start(message):
    print('%s (%s): %s' %(message.chat.first_name, message.chat.username, message.text))
    msg = None

    if message.text.lower() == '/start':
        msg = bot.send_message(message.chat.id, START_MESSAGE, parse_mode='markdown')

    elif message.text.lower() == '/help':
        msg = bot.send_message(message.chat.id, HELP_MESSAGE, parse_mode='markdown')
        
    if (msg):
        print('Бот: %s'%msg.text)

# Обработчик всех сообщений
@bot.message_handler(func = lambda message: True)
def answer_to_user(message):
    print('%s (%s): %s' %(message.chat.first_name, message.chat.username, message.text))
    msg = None

    user_message = message.text.lower()

    if BOT_NAME:
        regex = re.compile(BOT_NAME.lower())
        print(regex.search(user_message))
        if regex.search(user_message) == None:
            return

        regex = re.compile('%s[^a-z]'%(BOT_NAME.lower()))
        user_message = regex.sub("", user_message)

    user_message = user_message.lstrip()
    user_message = user_message.rstrip()
    
    print(user_message)

    if user_message == 'привет':
        msg = bot.send_message(message.chat.id, '*Привет, %s*'%(message.chat.first_name), parse_mode='markdown')

    elif user_message == 'помощь':
        msg = bot.send_message(message.chat.id, HELP_MESSAGE, parse_mode='markdown')

    else:
        try:
            answer = str(eval(user_message.replace(' ', '')))
            msg = bot.send_message(message.chat.id, user_message.replace(' ', '') + ' = ' + answer)
                
        except SyntaxError:
            msg = bot.send_message(message.chat.id, 'Похоже, что вы написали что-то не так. \nИсравьте ошибку и повторите снова')
        except NameError:
            msg = bot.send_message(message.chat.id, 'Переменную которую вы спрашиваете я не знаю. \nИсравьте ошибку и повторите снова')
        except TypeError:
            msg = bot.send_message(message.chat.id, 'Мне кажется, что в выражении присутствует ошибка типов. \nИсравьте ошибку и повторите снова')
        except ZeroDivisionError:
            msg = bot.send_message(message.chat.id, 'В выражении вы делите на ноль. \nИсравьте ошибку и повторите снова')

    if (msg):
        print('Бот: %s'%msg.text)

# Склонение существительных после числительных
def conv(n):
  es=['а', 'ов', '']
  n = n % 100
  if n>=11 and n<=19:
    s=es[1]
  else:
    i=n%10
    if i == 1:
      s=es[2]
    elif i in [2,3,4]:
      s=es[0]
    else:
      s=es[1]
  return s

# Обработчик картинок
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    #получаем user_id чтобы можно было сохранять файлы под user_id пользователя
    user_id = message.from_user.id

    sent_message = bot.send_message(message.chat.id, '\U0001F7E1 \U0001F7E1 \U0001F7E1 \U0001F7E1 \U0001F7E1')

    # скачиваем фотографию
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохраняем фотографию - в YOLO не понял как передать объектом не сохраняя
    src = '/code/received/' + str(user_id)+'.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
 
    bot.edit_message_text("\U0001F7E2 \U0001F7E1 \U0001F7E1 \U0001F7E1 \U0001F7E1",  chat_id=message.chat.id, message_id=sent_message.message_id)
  
    # Загружаем кастомную модель распознования
#    model = YOLO("yolo11n.pt")
    model = YOLO("/code/model_best.pt")

    bot.edit_message_text('\U0001F7E2 \U0001F7E2 \U0001F7E1 \U0001F7E1 \U0001F7E1',  chat_id=message.chat.id, message_id=sent_message.message_id)
    
    #Скармливаем картинку YOLO
    results = model.predict(src, max_det=500)

    bot.edit_message_text('\U0001F7E2 \U0001F7E2 \U0001F7E2 \U0001F7E1 \U0001F7E1',  chat_id=message.chat.id, message_id=sent_message.message_id)


    # Получаем описывающие рамки распознанного
    for result in results:
      boxes = result.boxes

    # Средний размер объекта - будем отбрасывать 0.5*avg<<2*avg
    average_values=[sum(x)/len(x) for x in zip(*boxes.xywh.tolist())]
    average_roll_size = (average_values[2]+average_values[3])/2

    # Счетчик хорошо распознанных
    roll_counter=0

    bot.edit_message_text('\U0001F7E2 \U0001F7E2 \U0001F7E2 \U0001F7E2 \U0001F7E1',  chat_id=message.chat.id, message_id=sent_message.message_id)

    # Скармливаем картинку Pillow чтобы дорисовывать
    photo = Image.open(src)
     
    # make the image editable
    draw = ImageDraw.Draw(photo, "RGBA")

    black = (3, 8, 12)
    
    # Шрифт надписей
    font = ImageFont.truetype("/code/RobotoMono-Regular.ttf", average_roll_size/3)
    
    # На распознанном рисуем и увеличиваем счетчик хорошо распознанного
    for i in range(len(boxes.xywh.tolist())):
      if (boxes.xywh.tolist()[i][2]>0.75*average_roll_size 
        and boxes.xywh.tolist()[i][2]<1.7*average_roll_size 
        and boxes.xywh.tolist()[i][3]>0.75*average_roll_size 
        and boxes.xywh.tolist()[i][3]<1.7*average_roll_size):
            roll_counter=roll_counter+1
            msg = str(roll_counter)
            draw.ellipse((boxes.xywh.tolist()[i][0]-0.75/2*boxes.xywh.tolist()[i][2],boxes.xywh.tolist()[i][1]-0.75/2*boxes.xywh.tolist()[i][3],
              boxes.xywh.tolist()[i][0]+0.75/2*boxes.xywh.tolist()[i][2],boxes.xywh.tolist()[i][1]+0.75/2*boxes.xywh.tolist()[i][3]), 
              fill=(200, 100, 0, 127))
            draw.text((boxes.xywh.tolist()[i][0],boxes.xywh.tolist()[i][1]), msg, anchor="mm", fill=black, font=font)

    bot.edit_message_text('\U0001F7E2 \U0001F7E2 \U0001F7E2 \U0001F7E2 \U0001F7E2',  chat_id=message.chat.id, message_id=sent_message.message_id)

    # Результат сохраняем
    photo.save(src[:-4]+"_result.jpg")

    result = open(src[:-4]+"_result.jpg", 'rb')

    bot.delete_message(message.chat.id, sent_message.message_id)
    
    bot.send_photo(message.chat.id, result, caption='Распознано '+str(roll_counter)+' рулончик{}'.format(conv(roll_counter)))
    
    #Удаление файлов
    os.remove(src)
    os.remove(src[:-4]+"_result.jpg")

# Вход в программу
if (__name__ == '__main__'):
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print ('Ошибка подключения. Попытка подключения через %s сек.'%TIMEOUT_CONNECTION)
            time.sleep(TIMEOUT_CONNECTION)
