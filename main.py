from random import choice
import telebot
import json
import atexit
from datetime import datetime
import re

from telebot import types
#from telegram import InlineKeyboardButton, InlineKeyboardMarkup



# -----------------Создаем клавиатуру с кнопками-------------------

keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

start_button = types.KeyboardButton('/start')
help_button = types.KeyboardButton('/help')
add_button = types.KeyboardButton('/add')
random_button = types.KeyboardButton('/random')
show_button = types.KeyboardButton('/show')
restart_button = types.KeyboardButton('/restart')
clear_tasks_button = types.KeyboardButton('/clearTasks')
exit_button = types.KeyboardButton('/exitsave')

# Добавьте кнопки на клавиатуру
keyboard.add(start_button, help_button)
keyboard.add(add_button, random_button)
keyboard.add(show_button, restart_button)
keyboard.add(clear_tasks_button, exit_button)

# -----------------Создаем клавиатуру с кнопками--------------Конец---



#-------------------------------СТАТУСЫ--------------------------------
# Словарь для хранения состояний пользователей

user_states = {}

# Константы для состояний
STATE_NONE = 'none'
STATE_ADD_TASK = 'add_task'
STATE_SHOW_TASKS = 'show_tasks'


def set_state(user_id, state, attempts=0):
    if user_id not in user_states:
        user_states[user_id] = {}
    user_states[user_id]['state'] = state
    user_states[user_id]['attempts'] = attempts
    if todos is not None:
        user_states[user_id]['todos'] = todos
    user_states[user_id]['attempts'] = attempts


# Получение текущего количества попыток
def get_attempts(user_id):
    return user_states[user_id].get('attempts', 0)


# Увеличение попыток для пользователя
def increment_attempts(user_id):
    if user_id in user_states:
        user_states[user_id].setdefault('attempts', 0)
        user_states[user_id]['attempts'] += 1

# Сброс попыток при начале новой сессии
def reset_attempts(user_id):
    if user_id in user_states:
        user_states[user_id]['attempts'] = 0


def get_user_state(user_id):
    return user_states.get(user_id, {}).get('state', STATE_NONE)


def reset_state(user_id):
    if user_id in user_states:
        user_states[user_id] = {}

#-------------------------------СТАТУСЫ---------------------Конец----




#---------------------------Проверка на Админа--------------------------
#Проверка на наличие и ддобавление пользователя в файл todos-------------

# Список администраторов
admin_list = [1588197954]  # Замените на реальные ID администраторов


def add_access(user_id):
    data = load_todos()  # Загружаем текущие задачи
    user_id = str(user_id)
    print(user_id)
    if user_id not in data:
        data[user_id] = {}  # Добавляем нового пользователя в словарь задач
        save_todos(data)  # Сохраняем обновленный словарь задач
        print(f"Добавлен пользователь с ID {user_id} в файл todos.json")
    else:
        print(f"Пользователь с ID {user_id} уже существует в файле todos.json")


def is_admin(user_id):
    return user_id in admin_list

#---------------------------Проверка на Админа-----------------------Конец
#Проверка на наличие и ддобавление пользователя в файл todos---------Конец




#------------РАБОТА С ФАЙЛОМ И ЗАДАЧАМИ-------------------------------------
#------------РАБОТА С ФАЙЛОМ И ЗАДАЧАМИ-------------------------------------
#------------РАБОТА С ФАЙЛОМ И ЗАДАЧАМИ-------------------------------------



# -----------Обьявление Функции Загрузить задачи из файла--------------------

def load_todos():
    try:
        with open('todos.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        print("Задачи загружены из файла:")  # Добавлено логирование
        return data
    except FileNotFoundError:
        print("Файл todos.json не найден")
        return {}  # Если файл не существует, возвращаем пустой словарь
    except json.JSONDecodeError:
        print("Не удалось декодировать файл 'todos.json'")
        return {}  # Если файл некорректен, возвращаем пустой словарь

# -----------Обьявление Функции Загрузить задачи из файла--------------------



# ---------------Обьявление Функции Сохранить задачи в файл------------------

def save_todos(todos):

    with open('todos.json', 'w', encoding='utf-8') as file:
        # Сохраняем объединенные данные как JSON
        json.dump(todos, file, ensure_ascii=False, indent=4)
    print("Задачи сохранены:")  # Добавлено логирование
# ---------------Обьявление Функции Сохранить задачи в файл------------------



#-------------Функция для проверки корректности формата даты------------------

def is_valid_date_format(date_string):
    try:
        datetime.strptime(date_string, '%d.%m.%y')
        return True
    except ValueError:
        return False



#------------------------AddToDo-добавляем задачу в файл-----------------------

# Функция для добавления задачи
def add_todo(user_id, date, task):
    # Загружаем существующие задачи
    todos = load_todos()
    # Добавляем логирование для отладки
    print(f"Загруженные задачи: {todos}")


    # Проверяем, есть ли пользователь с данным chat_id в файле
    if user_id not in todos:
        print(f"Ошибка: Пользователь {user_id} не найден в файле.")
        return "Ошибка: Пользователь не найден в файле."

    date = date.replace('/', '.')  # Заменить слэши на точки
    date = date.lower()


    if date == 'сегодня' or '!':
        # Получаем текущую дату
        today = datetime.now().strftime('%d.%m.%y')
        date = today

    if is_valid_date_format(date):
        if date not in todos[user_id]:
            print(f' Добавляем долбаную дату {date} в словарь пользователя с пустым значением ')
            todos[user_id][date] = []

        # Проверяем, что задача не повторяется
        if task not in todos[user_id][date]:
            todos[user_id][date].append(task)
            print(f'Если задача {task} не повторяется Добавляем задачу на эту дату ')
            save_todos(todos)  # Сохраняем задачи после добавления
            print(f"Задача '{task}' добавлена на дату {date} для пользователя {user_id}.")
        else:
            return f"Задача '{task}' уже существует на дате {date}."
    else:
        print(f"Некорректный формат даты: {date} для пользователя {user_id}.")
        return f"Некорректный формат даты: {date}"

#------------------------AddToDo-добавляем задачу в файл--------------Конец---
#------------РАБОТА С ФАЙЛОМ И ЗАДАЧАМИ-------------------------------Конец---




#----------------------------MAIN-- БЛОК-------------------------------------------
#----------------------------MAIN-- БЛОК-------------------------------------------
#----------------------------MAIN-- БЛОК-------------------------------------------

# Объявление глобальной переменной todos
todos = {}

# Вызов Функции Загрузить задачи
todos = load_todos()

#Проверочные принты
#print("PRIIIVEEEEET")
#print(todos)

#------------------Инициализация бота--------------------------

token = '6136409665:AAFB7w_7Rhmek-mlTAb_ssNWjh5vlMjmPbI'

bot = telebot.TeleBot(token)

#keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)


# -----------------------Список случайных задач-----------------------

RANDOM_TASKS = ['Позаниматься спортом, гирькой турничек', 'Кодить на  Python', 'Поучить сетевой Курс по Зуксель', 'Посмотреть Какой-то сериальчик', 'Поготовить\Вкусно поесть' , 'Прогуляться пешком или на велике']

#----------------------------MAIN-- БЛОК----------------------------------Конец-



### ---БЛОК ОБРАБОТЧИКОВ КОМАНД HANDLERS---------------------------------------
### ---БЛОК ОБРАБОТЧИКОВ КОМАНД HANDLERS---------------------------------------
### ---БЛОК ОБРАБОТЧИКОВ КОМАНД HANDLERS---------------------------------------




#----------Обработчик и функции--------Help------------------------------------


@bot.message_handler(commands=['help'])
def show_help(message):
    help_message = '''
Правила ввода задач:
1. Для запуска программы используйте команду: /start
2. Для добавления задачи или дня Рождения на определенную дату используйте команду: /add
   (можно кнопкой /add ) Потом Вас попросят выбрать внести задачу или День Рождения.
   Задачу или ДР можно внести на определенную дату, например 12.12.24
   Вас попросят написать саму задачу или ФИО именинника текстом, например: Сделать домашнее задание или Петров Василий Иванович

2. Для удаления задачи на определенной дате используйте команду: /delete дата задача
   Пример: /delete 31.12.22 Сделать домашнее задание (Функция  в разработе)

3. Для баловства или если вы не знаете чем заняться сегодня можете выбрать команду /random
   И бот придумает для Вас задачу из имеющихся и выведет три на выбор (Надо проработать возможность дополнять такой список)

4. Для просмотра задач на определенной дате используйте команду: /show
   - потом Вас попрсят ввести лату в формате xx.xx.xx - будут выведены задачи на данную дату
   -наряду с датой в формате xx.xx.xx Вы  также вы можете набрать "все" или просто "." - если хотите просмотреть задачи на все даты (без кавычек)
   -либо написать название месяца и года в формате xx.xx, например 03.24, если хотите получить все задачи на данный месяц данного года
   -также Вы можете ввести просто название месяца или номер, если хотите получить все дни рождения в этом месяце любого года разумеется ( в разработке)
   если вы наберете "сегодня" или "!" то  выйдут задачи на сегодняшний день

Формат даты: Дата должна быть в формате xx.xx.xx,  --  день.месяц.год. для получения задач на дату
Пример правильного формата даты: 31.12.22
Или для получения задач на конкретный месяц xx.xx
Пример правильного формата месяца года : 12.22
Пример правильного формата месяца для списка ДР в этом месяце : 12 или декабрь
Пример правильного задач на сегодня: "сегодня" или "!"
Вы также можете нажать на кнопку с нужной командой и потом ввести дату и задачу
'''
    bot.send_message(message.from_user.id, help_message)


HELP = '''
Список доступных команд:
/show  - напечать все задачи на заданную дату
/add - добавить задачу
/random - добавить на сегодня случайную задачу
/help - Напечатать help
/delete  - Удалить задачу
'''
#----------Обработчик и функции------Help----------------Конец-------------




#START-----Обработчик и функции------------START------------------------START
# Обработчик сообщений для обработки запросов пользователей на доступ к чату


@bot.message_handler(commands=['start'])
def handle_start(message):
    todos = load_todos()
    print(todos)
    user_id = str(message.from_user.id)
    print(user_id)
    if user_id in todos:

        print(f"Sending keyboard to user {user_id}")
        print(f"Пользователь {message.from_user.first_name} айди {user_id} уже имеет доступ к чату.")

        print(f"Задачи для пользователя с ID {user_id}:")
        for date, tasks in todos[user_id].items():
            print(f"Дата: {date}")
            for task in tasks:
                print(f" - {task}")


        bot.reply_to(message, f"Привет, {message.from_user.first_name}!", reply_markup=keyboard)
        bot.send_message(user_id, "Можешь добавить задачу в планнер на нужную дату или рандомную на сегодня получить ))  или вывести уже имеющиеся на какую-то дату или за месяц или все сразу:", reply_markup=keyboard)
        reset_state(message)
    else:
        print(f"Пользователь {message.from_user.first_name} с айди {user_id} запрашивает доступ к чату.")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Да', 'Нет')
        msg = bot.reply_to(message, "Вас нет в списке доступа к данному чату. Хотите отправить запрос администратору?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_access_request, user_id)


# Обработчик запроса доступа
def process_access_request(message, user_id):
    if message.text.lower() == 'да':
        print(f"Пользователь {message.from_user.first_name} отправил запрос на доступ к чату.")
        # Отправка запроса администратору
        for admin_id in admin_list:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Да', 'Нет')
            bot.send_message(admin_id, f"Пользователь {message.from_user.first_name} с ID {user_id} хочет присоединиться к чату. Одобрить запрос?", reply_markup=markup)
        bot.reply_to(message, "Ваш запрос отправлен администратору. Ожидайте ответа.")
    else:
        print(f"Пользователь {message.from_user.first_name} отказался отправлять запрос на доступ к чату.")
        bot.reply_to(message, "Обращайтесь еще.")


# Обработчик сообщений для обработки ответов администраторов
@bot.message_handler(func=lambda message: message.text.lower() in ['да', 'нет'])
def process_admin_response(message):
    if message.text.lower() == 'да':
        # Извлекаем user_id пользователя, который отправил запрос
        user_id = message.reply_to_message.text.split()[-1].strip('.')
        print(f"Администратор {message.from_user.first_name} принял запрос на доступ пользователя с ID {user_id}.")
        # Добавление пользователя в список доступа
        add_access(user_id)  # Добавляем пользователя в файл todos.json
        # Отправка сообщения пользователю
        bot.send_message(user_id, f'Вас {user_id} добавили в список доступа к чату. Приветствую!', reply_markup=keyboard)
        # Уведомление администраторов
        for admin_id in admin_list:
            if admin_id != message.from_user.id:  # Проверка, чтобы администратор не получил свое сообщение
                bot.send_message(admin_id, f"Пользователь с ID {user_id} добавлен в список доступа.", reply_markup=keyboard)
    else:
        # Извлекаем user_id пользователя, который отправил запрос
        user_id = message.reply_to_message.text.split()[-1].strip('.')
        print(f"Администратор {message.from_user.first_name} отклонил запрос на доступ пользователя с ID {user_id}.")
        bot.send_message(user_id, "Вам не добавлен в список доступа к чату.")


#---------Обработчик и функции----START------------------------Конец-------------




#RANDOM------Обработчик и функции-----RANDOM--------------------------RANDOM----

@bot.message_handler(commands=['random'])
def random(message):
    user_id = str(message.from_user.id)
    todos = load_todos()  # Загружаем задачи из файла

    if user_id in todos:

        tasks = [choice(RANDOM_TASKS) for _ in range(3)]  # Генерируем 3 случайные задачи
        tasks_text = "\n".join(f"{i + 1}. [ ] {task}" for i, task in enumerate(tasks, start=1))

        bot.send_message(message.from_user.id, f'Случайные задачи на сегодня:\n{tasks_text}', reply_markup=keyboard)
        #bot.send_message(message.from_user.id, f'Задачи "{tasks}" добавлена на сегодня', reply_markup=keyboard)
        reset_state(message)  # Сбрасываем состояние пользователя
    else:
        bot.send_message(message.from_user.id, 'У вас нет доступа к чату.', reply_markup=keyboard)
        reset_state(user_id)  # Сбрасываем состояние пользователя

#--------------Обработчик и функции---RANDOM-------------------Конец------------




#---ADD----------Обработчик и функции---ADD----------------------------ADD---

@bot.message_handler(commands=['add'])
def add(message):
    user_id = str(message.from_user.id)
    todos = load_todos()

    if user_id in todos:
        bot.send_message(message.from_user.id, 'Что вы хотите добавить?\n1. Задача\n2. День рождения')
        bot.register_next_step_handler(message, handle_add_choice)
    else:
        bot.send_message(message.from_user.id, 'У вас нет доступа к чату.', reply_markup=keyboard)



def handle_add_choice(message):
    user_id = str(message.from_user.id)
    choice = message.text.strip()

    # Инициализация счетчика попыток, если он не существует
    if user_id not in user_states:
        user_states[user_id] = {'attempts': 0}
    elif 'attempts' not in user_states[user_id]:
        user_states[user_id]['attempts'] = 0


    if choice == '1':
        user_states[user_id] = {'date': None, 'state': 'add_date'}
        bot.send_message(message.from_user.id, 'Для добавления задачи введите дату в формате xx.xx.xx:', reply_markup=keyboard)
        bot.register_next_step_handler(message, add_date)

    elif choice == '2':
        user_states[user_id] = {'state': 'add_birthday'}
        bot.send_message(message.from_user.id, 'Введите дату дня рождения в формате xx.xx:', reply_markup=keyboard)

        print("Дата дня рождения принята")
        bot.register_next_step_handler(message, add_birthday_date)

    else:
        user_states[user_id]['attempts'] += 1
        if user_states[user_id]['attempts'] >= 3:
            bot.send_message(message.from_user.id, 'Вы превысили количество попыток. Программа будет перезапущена.')
            reset_state(user_id)  # Функция для сброса состояния пользователя
            bot.send_message(message.from_user.id, 'Программа перезапущена. Введите команду /start для начала работы.')
        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, введите 1 или 2.')
            bot.register_next_step_handler(message, handle_add_choice)


def is_valid_birthday_format(date_str):
    return re.match(r'^\d{2}\.\d{2}\.\d{2}$', date_str) is not None



def add_birthday_date(message):
    user_id = str(message.from_user.id)
    birthday_date = message.text.strip()

    if is_valid_birthday_format(birthday_date):
        user_states[user_id]['date'] = birthday_date  # Сохраняем дату в user_states
        bot.send_message(message.from_user.id, 'Введите имя для дня рождения:', reply_markup=keyboard)
        bot.register_next_step_handler(message, add_birthday_name)
    else:
        bot.send_message(message.from_user.id, 'Некорректный формат даты. Пожалуйста, введите дату в формате xx.xx.xx.', reply_markup=keyboard)
        bot.register_next_step_handler(message, add_birthday_date)

def add_birthday_name(message):
    user_id = str(message.from_user.id)
    birthday_name = message.text.strip()
    birthday_date = user_states[user_id]['date']

    add_birthday_to_user(user_id, birthday_date, birthday_name)
    bot.send_message(user_id, f'День рождения {birthday_name} на {birthday_date} успешно добавлен.', reply_markup=keyboard)
    reset_state(user_id)


def add_birthday_to_user(user_id, birthday_date, birthday_name):
    todos = load_todos()
    if user_id not in todos:
        todos[user_id] = {}
    if birthday_date not in todos[user_id]:
        todos[user_id][birthday_date] = []
    todos[user_id][birthday_date].append(f'ДР: {birthday_name}')
    save_todos(todos)

# Добавление задачи
def add_date(message):
    user_id = str(message.from_user.id)
    date = message.text  # Получаем введенную дату
    print(date)

    # Проверяем, есть ли user_id в user_states, инициализируем если нет
    if user_id not in user_states:
        user_states[user_id] = {}

    # Проверяем, если дата - это "!" (сегодня)
    if date == '!' or 'сегодня':
        date = datetime.now().strftime('%d.%m.%y')  # Устанавливаем сегодняшнюю дату

    if is_valid_date_format(date):
        # Инициализируем запись для пользователя, если ее нет
        if user_id not in user_states:
            user_states[user_id] = {}
        user_states[user_id]['date'] = date
        user_states[user_id]['state'] = 'add_task'  # Инициализируем состояние, если его нет

        bot.send_message(user_id, 'Теперь введите задачу:', reply_markup=keyboard)
        bot.register_next_step_handler(message, add_task)  # Зарегистрируйте следующий обработчик для ввода задачи
        print('Обработчик добавить задачу зарегистрирован')

    else:
        increment_attempts(user_id)
        attempts = get_attempts(user_id)

        if attempts >= 3:
            bot.send_message(user_id, 'Вы исчерпали количество попыток. Введите команду: /start, /show, /add, /help', reply_markup=keyboard)
            #keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            reset_state(user_id)
        else:
            bot.send_message(user_id, 'Некорректный формат даты. Пожалуйста, введите дату в формате xx.xx.xx:', reply_markup=keyboard)
            bot.register_next_step_handler(message, add_date)  # Повторно запросите дату, если она введена неверно



# Обработчик для ожидания ввода задачи после ввода даты
@bot.message_handler(func=lambda message: str(message.from_user.id) in user_states and user_states[str(message.from_user.id)].get('state') == 'add_task')
def add_task(message):
    user_id = str(message.from_user.id)
    print('Обработчик добавить задачу вызван')

    date = user_states[user_id]['date']
    print(f'А где мой принт в рот мне ноги {date}')
    task = message.text  # Получаем введенную задачу
    print(f'А где мой принт в рот мне ноги {task}')
    add_todo(user_id, date, task)  # Передаем user_id в функцию add_todo

    print("Задачи сохранены")
    print(todos)
    bot.send_message(user_id, f'Задача "{task}" добавлена на дату {date}', reply_markup=keyboard)
    print(todos[user_id])
    reset_state(user_id)


    bot.send_message(message.from_user.id, "Выберете действие", reply_markup=keyboard)


      # Возвращаемся к ожиданию новых команд
    bot.send_message(user_id, "Введите команду: /start, /show, /add, /help")


#--------------Обработчик и функции---ADD--------------------Конец------------




#SHOW--------Обработчик и функции ---SHOW---------------------------SHOW----

@bot.message_handler(commands=['show'])
def show_tasks(message):
    user_id = str(message.from_user.id)
    print(f"User ID in show_tasks: {user_id}")  # Добавлено логирование
    todos = load_todos()

    if user_id in todos:
        print(user_id)
        set_state(user_id, 'show_date', attempts=0)
        bot.send_message(user_id, 'Введите дату в формате xx.xx.xx для просмотра задач, или напишите "!" для просмотра задач на сегодня, или напишите "все" для просмотра всех задач, или xx.xx для получения задач на конкретный месяц конкретного года или  просто  номер месяца для получения ДР')
        bot.register_next_step_handler(message, handle_date_or_all, todos)
    else:
        bot.send_message(user_id, 'У вас нет задач.')


# Функция для обработки ввода даты или команды "все" или остальных вариантов ввода пользователя
def handle_date_or_all(message, todos):
    user_input = message.text.lower()
    user_id = message.from_user.id
    print(f"Todos received in handle_date_or_all: {todos}")  # Добавлено логирование


    # Принудительная инициализация состояния пользователя
    if user_id not in user_states:
        user_states[user_id] = {}

    attempts = get_attempts(user_id)
    if attempts >= 3:
        # Пользователь превысил три попытки ввода неверного формата даты
        bot.send_message(user_id, 'Вы превысили количество попыток ввода неверного формата даты. Введите команду: /start, /show, /add, /help')
        reset_state(user_id)  # Сброс состояния пользователя

        return

  # Проверка на другие команды
    if user_input in ['/start', '/restart', '/exitsave', '/help']:
        handle_command(message)
        return

    # Check if input is 'все' or '.' for all tasks
    if user_input == 'все' or user_input == '.':
        print("Пользователь хочет увидеть все свои задачи")
        show_all_tasks(message, todos)
        reset_state(user_id)
    elif is_valid_date_format(user_input):
        handle_date(message, user_input, todos)

    elif re.match(r'^\d{2}\.\d{2}$', user_input):
        month_number, year_number = user_input.split('.')
        show_tasks_for_month_and_year(message, month_number, year_number, todos)

    elif user_input in ['сегодня', '!']:
        print("Пользователь хочет увидеть все свои задачи на сегодня")
        show_tasks_for_today(message, todos)
    elif user_input in ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']:
        month_number = get_month_number(user_input)
        print(f' Пользователь хочет увидеть все свои задачи на {month_number}')
        show_tasks_for_month(message, month_number, todos)
    elif user_input in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        month_number = user_input
        print(f' Пользователь хочет увидеть все свои задачи на {month_number}')
        show_tasks_for_month(message, month_number, todos)


    else:
        # Некорректный ввод даты, увеличиваем счетчик попыток
        increment_attempts(user_id)
        attempts = get_attempts(user_id)

        if attempts >= 3:
            bot.send_message(user_id, 'Вы исчерпали количество попыток. Введите команду: /start, /show, /add, /help')
            reset_state(user_id)

        else:
            bot.send_message(user_id, 'Некорректный формат даты. Пожалуйста, введите дату в формате xx.xx.xx.')
            bot.register_next_step_handler(message, handle_date_or_all, todos)
            return

    # Возвращаемся к ожиданию новых команд
    bot.send_message(user_id, "Введите команду: /start, /show, /add, /help")


# Функция для обработки введенной даты и вывода дзадач на эту дату
def handle_date(message, date, todos):
    user_id = str(message.from_user.id)  # Приводим user_id к строке
    print(user_id)
    todos = load_todos()

    print(f"Загруженные задачи Добавлено логирование: {todos}")  # Добавлено логирование


    if user_id in todos:
        print(f"Пользователь {user_id} найден в данных.")
        if date in todos[user_id]:
            print(f"Дата {date} найдена в данных пользователя {user_id}.")
            #tasks = todos[user_id][date]
            tasks = [task for task in todos[user_id][date] if not task.startswith('ДР:')]
            print(f"Задачи на {date}: {tasks}")  # Добавлено логирование
            tasks_text = "\n".join(f"- {task}" for task in tasks)

            print(f"Отправляем пользователю его задачи {date}: {tasks}")  # Добавлено логирование
            bot.send_message(message.chat.id, f"Задачи на {date}:\n{tasks_text}")
        else:
            print(f"Дата {date} не найдена в данных пользователя {user_id}.")
            bot.send_message(message.from_user.id, f"На {date} задач нет.")
    else:
        print(f"Пользователь {user_id} не найден в данных.")
        bot.send_message(message.from_user.id, f"Пользователь {user_id} не найден в данных.")

    reset_state(user_id)  # Сброс состояния пользователя

# Функция для показа всех задач на сегодня
def show_tasks_for_today(message, todos):
    user_id = str(message.from_user.id)
    today = datetime.now().strftime('%d.%m.%y')
    print(f'User ID: {user_id}, Today: {today}')

    todos = load_todos()
    print(f'Задачи загружены из файла: {todos}')

    if user_id in todos:
        if today in todos[user_id]:
            tasks = [task for task in todos[user_id][today] if not task.startswith('ДР:')]
            tasks_text = "\n".join(f"- {task}" for task in tasks)
            bot.send_message(message.chat.id, f"Задачи на сегодня ({today}):\n{tasks_text}")
        else:
            bot.send_message(message.chat.id, f"На сегодня ({today}) задач нет.")
    else:
        bot.send_message(message.chat.id, f"Пользователь {user_id} не найден в данных.")

    reset_state(user_id)  # Сброс состояния пользователя

# Функция для показа всех задач пользователя
def show_all_tasks(message, todos):
    user_id = str(message.from_user.id)
    print(user_id)
    todos = load_todos()
    print(todos)
    all_tasks_text = ""


     # Получаем задачи пользователя
    user_tasks = todos.get(user_id, {})
    print(f'User Tasks: {user_tasks}')
    print("ПРОВЕРКА ПРИНТА")

    # Сортируем даты перед выводом задач

#    sorted_dates = sorted(todos.get(str(user_id), {}).items(), key=lambda x: tuple(map(int, x[0].split('.'))))

    if user_tasks:
        # Сортируем даты перед выводом задач
        try:
            sorted_dates = sorted(user_tasks.items(), key=lambda x: datetime.strptime(x[0], '%d.%m.%y'))
        except ValueError as e:
            print(f'Ошибка сортировки дат: {e}')
            bot.send_message(user_id, "Произошла ошибка при сортировке дат.")
            return

        for date, tasks in sorted_dates:
            all_tasks_text += f'Задачи на {date}:\n'
            all_tasks_text += "\n".join(f" - {task}" for task in tasks)
            all_tasks_text += "\n\n"

        print(f'All Tasks Text: {all_tasks_text}')
        bot.send_message(user_id, all_tasks_text)
    else:
        bot.send_message(user_id, "Задач пока нет.")

    reset_state(user_id)  # Сброс состояния пользователя



# Функция для показа задач за определенный месяц и год
def show_tasks_for_month_and_year(message, month_number, year_number, todos):
    user_id = str(message.from_user.id)
    user_tasks = todos.get(user_id, {})  # Получаем задачи конкретного пользователя

    # Создаем список для хранения задач за указанный месяц и год
    month_tasks = []

    # Проходим по всем датам и задачам пользователя
    for date, tasks in user_tasks.items():
        # Разбиваем дату на составляющие: день, месяц, год
        day, task_month, task_year = date.split('.')

        # Проверяем соответствие месяца и года
        if task_month == month_number and task_year == year_number:
            # Если дата соответствует, добавляем задачи в список month_tasks
            month_tasks.extend(tasks)

    # Формируем текст с задачами для отправки пользователю
    if month_tasks:
        tasks_text = "\n".join(f"{i + 1}. - {task}" for i, task in enumerate(month_tasks, start=1))
        response_text = f'Задачи за {get_month_name(month_number)} {year_number}:\n{tasks_text}'
    else:
        response_text = f'Задач за {get_month_name(month_number)} {year_number} нет.'

    # Отправляем сообщение пользователю с задачами за указанный месяц и год
    bot.send_message(user_id, response_text)

    # Сбрасываем состояние пользователя
    reset_state(user_id)



# Функция для показа задач за определенный месяц
def show_tasks_for_month(message, month_number, todos):
    print(f'Вызвана функция показа задач за конкретный месяц {month_number}')
    user_id = str(message.from_user.id)

    user_tasks = todos.get(user_id, {})

    month_tasks = []
    print(month_tasks)


    print(f"User ID in show_tasks_for_month: {user_id}")  # Добавлено логирование
    print(f"User tasks: {user_tasks}")  # Логирование данных пользователя

    for date, tasks in user_tasks.items():
        print(f"Логирование проверки даты: {date}, month: {date.split('.')[1]}, month_number: {month_number}")  # Логирование проверки даты
        task_month = date.split('.')[1]
        if task_month == month_number:
            month_tasks.extend([task for task in tasks if task.startswith('ДР:')])
            #month_tasks.extend(tasks)
            print(f"Логирование найденных задач {date}: {tasks}")  # Логирование найденных задач

    if month_tasks:
        tasks_text = "\n".join(f"{i + 1}. - {task}" for i, task in enumerate(month_tasks, start=1))
        bot.send_message(user_id, f'Задачи за {get_month_name(month_number)}:\n{tasks_text}')
    else:
        bot.send_message(user_id, f'Задач или Дней Рождения за {get_month_name(month_number)} нет.')

    reset_state(user_id)  # Сброс состояния пользователя

# Функция для получения номера месяца по его названию
def get_month_number(month_name):
    months = {
        'январь': '01',
        'февраль': '02',
        'март': '03',
        'апрель': '04',
        'май': '05',
        'июнь': '06',
        'июль': '07',
        'август': '08',
        'сентябрь': '09',
        'октябрь': '10',
        'ноябрь': '11',
        'декабрь': '12'
    }
    return months.get(month_name, '')

# Функция для получения названия месяца по его номеру
def get_month_name(month_number):
    months = {
        '01': 'январь',
        '02': 'февраль',
        '03': 'март',
        '04': 'апрель',
        '05': 'май',
        '06': 'июнь',
        '07': 'июль',
        '08': 'август',
        '09': 'сентябрь',
        '10': 'октябрь',
        '11': 'ноябрь',
        '12': 'декабрь'
    }
    return months.get(month_number, '')


def handle_command(message):
    user_input = message.text.lower()
    if user_input == '/start':
        handle_start(message)
    elif user_input == '/restart':
        restart_command(message)
    elif user_input == '/exitsave':
        exit_program(message)
    elif user_input == '/help':
        show_help(message)

#-------------------Обработчик и функции SHOW----------------Конец--------------



#CLEARTASK----Обработчик и функция-------CLEARTASK----------------------CLEARTASK--


@bot.message_handler(commands=['clearTasks'])
def handle_clear_tasks(message):
    user_id = str(message.from_user.id)  # Преобразование user_id в строку сразу
    bot.send_message(user_id, "Вы точно хотите удалить все свои задачи и дни рождения?\n1. Удалить только задачи\n2. Удалить только дни рождения\n3. Удалить всю информацию")
    bot.register_next_step_handler(message, process_clear_choice, user_id)

#-----------Вопрос на уверенность пользователя в необходимости удаления информацииь----------
def process_clear_choice(message, user_id):
    choice = message.text.strip()
    if choice in ['1', '2', '3']:
        bot.send_message(user_id, "Вы уверены? Это действие нельзя отменить.\n1. Да\n2. Нет")
        bot.register_next_step_handler(message, process_final_confirmation, user_id, choice)
    else:
        bot.send_message(user_id, "Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")
        bot.register_next_step_handler(message, handle_clear_tasks)  # Перенаправляем обратно на handle_clear_tasks


#---------Функция выполнения подтверждения пользователя об удалении либо опровержение----------
def process_final_confirmation(message, user_id, choice):
    confirmation = message.text.strip().lower()
    if confirmation == '1':
        result = clear_tasks(user_id, choice)
        bot.send_message(user_id, result)
    elif confirmation == '2':
        bot.send_message(user_id, "Операция отменена.")
    else:
        bot.send_message(user_id, "Неверный ответ. Пожалуйста, ответьте '1' или '2'.")
        bot.register_next_step_handler(message, process_final_confirmation, user_id, choice)


#-------------Выполнение удаления  в зависимости от выбора пользователя что удалять-----------
def clear_tasks(user_id, choice):
    global todos
    user_id = str(user_id)
    print(f"Проверка пользователя {user_id} в todos: {todos}")  # Добавлено логирование

    if user_id in todos:
        if choice == '1':
            print("Выбрано 1")
            # Очищаем только задачи
            todos[user_id] = {date: [task for task in tasks if task.startswith('ДР:')] for date, tasks in todos[user_id].items()}
            message = "Все задачи удалены."
        elif choice == '2':
            print("Выбрано 2")
            # Очищаем только дни рождения
            todos[user_id] = {date: [task for task in tasks if not task.startswith('ДР:')] for date, tasks in todos[user_id].items()}
            message = "Все дни рождения удалены."
        elif choice == '3':
            # Очищаем все задачи и дни рождения
            todos[user_id] = {}
            print("Выбрано 3")
            message = "Вся информация удалена."
            print(f"Инфрмация  по выбору пользователя {user_id} только что очищена")
            return message

        save_todos(todos)  # Сохраняем обновленный список задач
        print(print(f"Инфрмация  по выбору пользователя {user_id} только что очищена"))
        return f"Задачи по выбору пользователя {user_id} только что очищены"
    else:
        print(f"Пользователь {user_id} не найден")
        return f"Пользователь {user_id} не найден"



#-----Обработчик и функция для кнопки очистки задач  /ClearTasks---------Конец------



#DELETE--------Обработчик и функции ----DELETE-------------------------DELETE-

@bot.message_handler(commands=['delete'])
def delete_task(message):
    bot.send_message(message.from_user.id, "Введите дату в формате xx.xx.xx, чтобы удалить задачи на эту дату:")
    user_states[message.from_user.id] = {'date': None, 'state': 'delete_date'}  # вот тут я исправил

# Добавьте следующий обработчик для ожидания ввода даты
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'delete_date')
def handle_delete_date(message):
    date = message.text
    tasks = todos.get(date, [])
    if tasks:
        bot.send_message(message.from_user.id, f"Список задач на {date}:\n" + "\n".join(f"{i + 1}. {task}" for i, task in enumerate(tasks)))
        bot.send_message(message.from_user.id, "Введите номер задачи, которую вы хотите удалить, или 0 чтобы удалить все задачи на эту дату:")
        user_states[message.from_user.id]['state'] = 'delete_task'  # вот тут я исправил
    else:
        bot.send_message(message.from_user.id, f"На {date} задач нет. Попробуйте другую дату.")
        user_states[message.from_user.id] = None  # вот тут я исправил

# Добавьте следующий обработчик для ожидания выбора номера задачи или 0
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'delete_task')
def handle_delete_task(message):
    date = message.text
    if date == '0':
        # Удалить все задачи на эту дату
        todos[user_states[message.from_user.id]] = []
        bot.send_message(message.from_user.id, "Все задачи на данную дату удалены.")
        reset_state(message)
    else:
        try:
            task_number = int(date)
            if task_number > 0 and task_number <= len(todos[user_states[message.from_user.id]]):
                # Удалить задачу по номеру
                deleted_task = todos[user_states[message.from_user.id]].pop(task_number - 1)
                bot.send_message(message.from_user.id, f"Задача \"{deleted_task}\" удалена.")
            else:
                bot.send_message(message.from_user.id, "Введите корректный номер задачи или 0 для удаления всех задач на эту дату.")
        except ValueError:
            bot.send_message(message.from_user.id, "Введите корректный номер задачи или 0 для удаления всех задач на эту дату.")
    reset_state(message)
#-----------------------------------------Delete------------------Конец---------




#RESTART----Обработчик и  Функция ------ RESTART------------------------RESTART--

@bot.message_handler(commands=['restart'])
def restart_command(message):
    user_id = str(message.from_user.id)
    reset_state(user_id)  # Сбрасываем состояние пользователя
    bot.send_message(user_id, "Состояние бота сброшено на стартовое.", reply_markup=keyboard)


#-----------Обработчик и  Функция ------ RESTART-------------------Конец-------




# EXITSAVE---------Обработчик и  Функция для команды /EXITSAVE-------------EXITSAVE
@bot.message_handler(commands=['exitsave'])
def exit_program(message):
    save_on_exit(todos)

   # Сохраняем состояния todos
    save_todos(todos)
    print("Задачи  сохранены в файлы")

    # Отправляем сообщение о завершении работы бота
    bot.send_message(message.from_user.id, 'Спасибо за использование! Задачи добавлены. До свидания!')


# Функция для сохранения задач и access_list при выключении
def save_on_exit(todos):
    try:
        # Сохраняем todos
        save_todos(todos)
        print("Задачи сохранены в файл")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")

# ----------Обработчик и  Функция для команды /exitsave---------Конец------------



# ----------Обработчик и  для произвольных симфолов от пользователя ----------
@bot.message_handler(func=lambda message: True)
def handle_random_input(message):
    user_id = message.from_user.id
    user_input = message.text.lower()

    if user_input not in ['/start', '/show', '/add', '/help']:
        bot.send_message(user_id, "Неизвестная команда. Введите /help для получения списка команд.")

# --------Обработчик и  для произвольных симфолов от пользователя ---Конец-----



# Регистрируем функцию save_on_exit для выполнения при завершении работы
atexit.register(save_on_exit, todos)



bot.polling(none_stop=True)
