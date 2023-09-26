import json
import telebot
import config

bot = telebot.TeleBot(config.TOKEN)
bot_username = config.username

queues=[]

"""Функции"""
"""Функции для работы с json файлом"""
def read():
    global queues
    with open("list.json") as f:
        queues = json.loads(f.read())

def write():
    global queues
    with open("list.json", 'w') as f:
        f.write(json.dumps(queues))

"""Функции для работы с очередями"""
def ind(s,queues):
    for i in range(len(queues)):
        if queues[i][0]==s:
            return i
    return 'net'

def add(mn,qn):
    global queues
    try:
        i = ind(qn,queues)
        if mn not in queues[i]:
            queues[i].append(mn)
    except:
        pass


def remove(mn,qn):
    global queues
    try:
        i = ind(qn, queues)
        queues[i].remove(mn)
    except:
        pass


def make(qn):
    queues.append([qn, ])
def delete(qn):
    global queues
    try:
        i = ind(qn, queues)
        queues.pop(i)
    except:
        pass
def mpos(mn,qn):
    global queues
    i = ind(qn, queues)
    try:
        return queues[i].index(mn)
    except:
        return 'net'

def ping(mn):
    global queues
    mass = []
    for i in range(len(queues)):
        try:
            mass.append([queues[i][0],str(queues[i].index(mn))])
        except:
            pass
    if len(mass)!=0:
        return mass
    return 'net'
"""Функции"""

read()

"""Команды бота"""
@bot.message_handler(commands=['test'])
def test(message):
     bot.send_message(message.chat.id, message)

@bot.message_handler(commands=['help'])
def help(message):
    s = ('/mq (нет аргумента) - узнать все свои очереди\n'
         '/aq (нет аргумента) - узнать все очереди\n'
         '/make (название очереди) - сделать новую очередь\n'
         '/del (название очереди)- удалить Всю очередь\n'
         '/add (название очереди)- добавить себя в очередь\n'
         '/rem (название очереди)- удалить себя из очереди\n'
         'Между командой и аргументом Должен быть пробел\n')
    bot.send_message(message.chat.id, s)

@bot.message_handler(commands=['myqueue','mq'])
def com1(message):
    if ping(str(message.from_user.id))!='net':
        mess = ping(str(message.from_user.id))
        print(mess)
        for i in range(len(mess)):
            s = message.from_user.first_name + ' ' + ' '.join(mess[i])
            bot.send_message(message.chat.id,s)
    else:
        s = 'тебя нет ни в одной очереди'
        bot.send_message(message.chat.id, s)

@bot.message_handler(commands=['add'])
def com2(message):
    qn = (message.text)[5:]
    add(str(message.from_user.id),qn)
    m = str(mpos(str(message.from_user.id),qn))
    if m != 'net':
        s = '@'+message.from_user.username + ' ' + m
        write()
        bot.send_message(message.chat.id,s)
    else:
        s = ('нет такой очереди\n'
             'назывния очередей должны полностью совпадать')
        bot.send_message(message.chat.id, s)

@bot.message_handler(commands=['rem'])
def com3(message):
    qn = (message.text)[5:]
    if mpos(str(message.from_user.id),qn) != 'net':
        remove(str(message.from_user.id), qn)
        write()
        s = 'удалил ' + message.from_user.first_name
        bot.send_message(message.chat.id, s)
    else:
        s = 'тебя там нет'
        bot.send_message(message.chat.id, s)

@bot.message_handler(commands=['make'])
def com4(message):
    qn = (message.text)[6:]
    if qn != "":
        if ind(qn, queues) == 'net':
            make(qn)
            s = 'сделал ' + qn
            bot.send_message(message.chat.id, s)
            add(str(message.from_user.id), qn)
            m = str(mpos(str(message.from_user.id), qn))
            s = message.from_user.first_name + ' ' + m
            write()
            bot.send_message(message.chat.id, m)
        else:
            s = 'уже есть такая очередь'
            bot.send_message(message.chat.id, s)
    else:
        s = 'Введите название очереди'
        bot.send_message(message.chat.id, s)

@bot.message_handler(commands=['del'])
def com5(message):
    qn = (message.text)[5:]
    if ind(qn,queues) != 'net':
        delete(qn)
        write()
        s = 'удалил очередь ' + qn
        bot.send_message(message.chat.id, s)
    else:
        s = 'нечего удалять'
        bot.send_message(message.chat.id, s)
@bot.message_handler(commands=['aq'])
def com6(message):
    read()
    try:
        mass = [[str(s[0])+' ',str(len(s)-1)] for s in queues]
        for i in range(len(mass)):
            mass[i] = mass[i][0] + '|' + '{' + mass [i][1] + '}'
        s = "\n".join(mass)
        bot.send_message(message.chat.id, s)
    except:
        s = 'ещё нет очередей'
        bot.send_message(message.chat.id, s)
bot.polling(none_stop=True)