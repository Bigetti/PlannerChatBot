from random import choice
import telebot
import json
import atexit
from datetime import datetime
import re

from telebot import types


# from config import add_access,  admin_list, remove_access, check_access


# -----------------Создаем клавиатуру с кнопками

keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

start_button = types.KeyboardButton('/start')
help_button = types.KeyboardButton('/help')
add_button = types.KeyboardButton('/add')
random_button = types.KeyboardButton('/random')
show_button = types.KeyboardButton('/show')
restart_button = types.KeyboardButton('/restart')
clear_tasks_button = types.KeyboardButton('/clear_tasks')
exit_button = types.KeyboardButton('/exitsave')



# Добавьте кнопки на клавиатуру
keyboard.add(start_button, help_button)
keyboard.add(add_button, random_button)
keyboard.add(show_button, restart_button)
keyboard.add(clear_tasks_button, exit_button)

#_______------СТАТУСЫ-----______________
# Словарь для хранения состояний пользователей

user_states = {}

# Константы для состояний
STATE_NONE = 'none'
STATE_ADD_TASK = 'add_task'
STATE_SHOW_TASKS = 'show_tasks'


# Предполагаемый код для установки состояния пользователя
def set_state(user_id, state):
    user_states[user_id]['state'] = state
    return True


# Функция для получения состояния пользователя
def get_user_state(user_id):

    # Используем метод get словаря user_states для получения значения по ключу user_id.
    # Если ключ не найден, возвращается пустой словарь {}.
    user_state_dict = user_states.get(user_id, {})

    # Используем метод get словаря user_state_dict для получения значения по ключу 'state'.
    # Если ключ 'state' не найден, возвращается константа STATE_NONE.
    user_state = user_state_dict.get('state', STATE_NONE)

    # Возвращаем полученное состояние пользователя.
    return user_state



# Функция для сброса состояния пользователя и отображения клавиатуры снова
def reset_state(message):
    user_id = message.from_user.id
    user_states[user_id] = STATE_NONE



#---------------Проверка на Админа----------Проверка на наличие поьзователя в файле-------------------

# Список администраторов
admin_list = [1588197954]  # Замените на реальные ID администраторов


def add_access(chat_id):
    data = load_todos()
    user_id = chat_id
    if user_id not in data:
        data[user_id] = {}
        save_todos(data)
        print(f"Добавлен пользователь с ID {user_id} в файл todos.json")
    else:
        print(f"Пользователь с ID {user_id} уже существует в файле todos.json")


def is_admin(user_id):
    return user_id in admin_list



# ----------Обьявление Функции Загрузить задачи из файла--------------------

def load_todos():
    try:
        with open('todos.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}  # Если файл не существует, возвращаем пустой словарь
    except json.JSONDecodeError:
        print("Не удалось декодировать файл 'todos.json'")
        return {}  # Если файл некорректен, возвращаем пустой словарь



# ---------------Обьявление Функции Сохранить задачи в файл---------------------

def save_todos(todos):
    # Загружаем старые данные из файла, если они есть
    old_todos = load_todos()

    # Объединяем старые данные с новыми данными
    old_todos.update(todos)

    # Записываем обновленные данные обратно в файл
    with open('todos.json', 'w', encoding='utf-8') as file:
        # Сохраняем объединенные данные как JSON
        json.dump(old_todos, file, ensure_ascii=False, indent=4)


#-------------Функция для проверки корректности формата даты------------------

def is_valid_date_format(date_string):
    try:
        datetime.strptime(date_string, '%d.%m.%y')
        return True
    except ValueError:
        return False



#-------------------------AddToDo----------------------------------

# Функция для добавления задачи
def add_todo(user_id, date, task):
    # Загружаем существующие задачи
    todos = load_todos()

    # Проверяем, есть ли пользователь с данным chat_id в файле
    if user_id not in todos:
        return "Ошибка: Пользователь не найден в файле."

    date = date.replace('/', '.')  # Заменить слэши на точки
    date = date.lower()

    if date == 'сегодня':
        # Получаем текущую дату
        today = datetime.now().strftime('%d.%m.%y')
        date = today

    if is_valid_date_format(date):
        if date not in todos[user_id]:
            todos[user_id][date] = []
        # Проверяем, что задача не повторяется
        if task not in todos[user_id][date]:
            todos[user_id][date].append(task)
            save_todos(todos)  # Сохраняем задачи после добавления
        else:
            return f"Задача '{task}' уже существует на дате {date}."
    else:
        return f"Некорректный формат даты: {date}"



#------------------------MAIN---------------------------

# Объявление глобальной переменной todos
todos = {}

# Вызов Функции Загрузить задачи
todos = load_todos()

print("PRIIIVEEEEET")
print(todos)

#Инициализация бота--------------------------

token = '6136409665:AAFB7w_7Rhmek-mlTAb_ssNWjh5vlMjmPbI'

bot = telebot.TeleBot(token)


# -----------------------Список случайных задач-----------------------

RANDOM_TASKS = ['Позаниматься спортом, гирькой турничек', 'Кодить на  Python', 'Поучить сетевой Курс по Зуксель', 'Посмотреть Какой-то сериальчик', 'Поготовить\Вкусно поесть' , 'Прогуляться пешком или на велике']



#---------------Help------------


@bot.message_handler(commands=['help'])
def show_help(message):
    help_message = '''
Правила ввода задач:
1. Для добавления задачи на определенную дату используйте команду: /add дата задачи
   (команду можно кнопкой)   Пример: /add 31.12.22
   Потом Вас попросят написать саму задачу текстом, например: Сделать домашнее задание

2. Для удаления задачи на определенной дате используйте команду: /delete дата задача
   Пример: /delete 31.12.22 Сделать домашнее задание (Функция  в разработе)

3. Для баловства или если вы не знаете чем заняться сегодня можете выбрать команду /random
   И бот придумает для Вас задачу из имеющихся (Надо проработать возможность дополнять такой список)

4. Для просмотра задач на определенной дате используйте команду: /show 12.02.21
   Также вы можете набрать "все" - если хотите просмотреть задачи на все даты
   либо "сегодня" - соответственно на сегодня
   либо написать название месяца (Эта чать функции show также пока в разработе)

Формат даты: Дата должна быть в формате xx.xx.xx,  --  день.месяц.год.
Пример правильного формата даты: 31.12.22
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


# Функция для обработки команды /restart
@bot.message_handler(commands=['restart'])
def restart_command(message):
    user_id = str(message.from_user.id)
    reset_state(message)  # Устанавливаем состояние пользователя в начальное состояние
    bot.send_message(user_id, "Бот был перезапущен. Выберите действие:", reply_markup=keyboard)



#----------------------------------Start-------------------------------------------------
# Обработчик сообщений для обработки запросов пользователей на доступ к чату


@bot.message_handler(commands=['start'])
def handle_start(message):
    todos = load_todos()
    user_id = str(message.from_user.id)
    print(user_id)
    if user_id in todos:
        print(f"Пользователь {message.from_user.first_name} айди {user_id} уже имеет доступ к чату.")
        bot.reply_to(message, f"Привет, {message.from_user.first_name}!")
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
            bot.send_message(admin_id, f"Пользователь {message.from_user.first_name} с ID {user_id} хочет присоединиться к чату. Отправить запрос?", reply_markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add('Да', 'Нет'))
        bot.reply_to(message, "Ваш запрос отправлен администратору. Ожидайте ответа.")
    else:
        print(f"Пользователь {message.from_user.first_name} отказался отправлять запрос на доступ к чату.")
        bot.reply_to(message, "Обращайтесь еще.")


# Обработчик сообщений для обработки ответов администраторов
@bot.message_handler(func=lambda message: message.text.lower() in ['да', 'нет'])
def process_admin_response(message):
    if message.text.lower() == 'да':
        print(f"Администратор {message.from_user.first_name} принял запрос на доступ пользователя с ID {message.from_user.id}.")
        # Добавление пользователя в список доступа
        add_access(message.chat.id)
        # Отправка сообщения пользователю
        bot.send_message(message.chat.id, f"Вас добавили в список доступа к чату. Приветствую, {message.from_user.first_name}!")
        # Уведомление администраторов
        for admin_id in admin_list:
            if admin_id != message.from_user.id:  # Проверка, чтобы администратор не получил свое сообщение
                bot.send_message(admin_id, f"Пользователь {message.from_user.first_name} с ID {message.from_user.id} добавлен в список доступа.")
    else:
        print(f"Администратор {message.from_user.first_name} отклонил запрос на доступ пользователя с ID {message.from_user.id}.")
        bot.send_message(message.chat.id, "Вам не добавлен в список доступа к чату.")


#-------------------------- Функция для перезапуска бота----------------------------
def restart_bot():
    global todos
    todos = load_todos()
    print("Задачи загружены из файла")


#----------------------------- Функция для проверки формата даты---------------------------

# def is_valid_date_format(date):
#     # Паттерн для проверки формата даты xx.xx.xx
#     pattern = r'^\d{2}\.\d{2}\.\d{2}$'
#     return re.match(pattern, date)


#------------------------------------Random------------------------------------------

@bot.message_handler(commands=['random'])
def random(message):
    user_id = str(message.from_user.id)
    global todos
    if user_id in todos:
        task = choice(RANDOM_TASKS)
        add_todo(user_id, 'сегодня', task)  # Добавляем задачу на "сегодня"
        bot.send_message(message.from_user.id, f'Задача "{task}" добавлена на сегодня')
        save_todos(todos)
    #    reset_user_state(message)  # Сбрасываем состояние пользователя
        reset_state(message)  # Сбрасываем состояние пользователя


#---------------------------------Add---------------------------------------------------------------------

@bot.message_handler(commands=['add'])
def add(message):
    user_id = str(message.from_user.id)
    if user_id in todos:
        user_states[message.from_user.id] = {'date': None, 'state': 'add_date'}
        bot.send_message(message.from_user.id, 'Введите дату в формате xx.xx.xx:')
        bot.register_next_step_handler(message, add_date)  # Зарегистрируйте следующий обработчик для ввода даты
    else:
        print("No such id in list")
        bot.send_message(message.from_user.id, 'No such id in list')

def add_date(message):
    user_id = str(message.from_user.id)
    date = message.text  # Получаем введенную дату
    if is_valid_date_format(date):
        # Инициализируем запись для пользователя, если ее нет
        if user_id not in user_states:
            user_states[user_id] = {}
        user_states[user_id]['date'] = date
        user_states[user_id]['state'] = 'add_task'  # Инициализируем состояние, если его нет
        bot.send_message(user_id, 'Теперь введите задачу:')
        bot.register_next_step_handler(message, add_task)  # Зарегистрируйте следующий обработчик для ввода задачи
    else:
        bot.send_message(user_id, 'Некорректный формат даты. Пожалуйста, введите дату в формате xx.xx.xx:')
        bot.register_next_step_handler(message, add_date)  # Повторно запросите дату, если она введена неверно

# Обработчик для ожидания ввода задачи после ввода даты
@bot.message_handler(func=lambda message: str(message.from_user.id) in user_states and user_states[str(message.from_user.id)].get('state') == 'add_task')
def add_task(message):
    user_id = str(message.from_user.id)
    global todos
    date = user_states[user_id]['date']
    task = message.text  # Получаем введенную задачу
    add_todo(user_id, date, task)  # Передаем user_id в функцию add_todo
    save_todos(todos)  # Сохраняем задачи после добавления
    bot.send_message(user_id, f'Задача "{task}" добавлена на дату {date}')
    print(todos)
    reset_state(message)


#---------------------------------------Show-----------------------------------------------


# Обработчик команды /show
@bot.message_handler(commands=['show'])
def show_tasks(message):
    user_id = str(message.from_user.id)  # Преобразуйте user_id в строку
    todos = load_todos()
    if user_id in todos:
        set_state(user_id, 'show_date')
        bot.send_message(user_id, 'Введите дату в формате xx.xx.xx для просмотра задач, или напишите "все" для просмотра всех задач.')
        bot.register_next_step_handler(message, handle_date_or_all)
    else:
        bot.send_message(user_id, 'У вас нет задач.')


# Обработчик для обработки даты или всех задач
@bot.message_handler(func=lambda message: user_states.get(str(message.from_user.id), {}).get('state') == 'show_date')
def handle_date_or_all(message):
    user_input = message.text.lower()
    user_id = message.from_user.id
    todos = load_todos()


    if user_input == 'все' or user_input == '.':
        show_all_tasks(message, todos)
        reset_state(message)
    elif is_valid_date_format(user_input):
        handle_date(message, user_input, todos)
    elif user_input == 'сегодня':
        handle_date(message, 'сегодня', todos)
    elif user_input in ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']:
        month_number = get_month_number(user_input)
        show_tasks_for_month(message, month_number, todos)
    elif user_input in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        month_number = user_input
        show_tasks_for_month(message, month_number, todos)
    elif user_input.startswith('/'):
        reset_state(message)
        return
    else:
        bot.send_message(user_id, 'Некорректный формат даты. Пожалуйста, введите дату в формате xx.xx.xx.')
        bot.register_next_step_handler(message, handle_date_or_all)



# Обработчик для обработки даты
def handle_date(message, date, todos):
    user_id = message.from_user.id
    user_states[user_id]['date'] = date

    # Получаем задачи для данной даты
    tasks = todos.get(user_id, {}).get(date, [])

    if tasks:
        tasks_text = "\n".join(f"{i + 1}. [ ] {task}" for i, task in enumerate(tasks, start=1))
        bot.send_message(message.chat.id, f'Задачи на {date}:\n{tasks_text}')
    else:
        bot.send_message(message.from_user.id, f'На {date} задач нет.')

    # Сбрасываем состояние пользователя
    user_states[user_id]['state'] = None


# Обработчик для показа задач за определенный месяц
def show_tasks_for_month(message, month_number, todos):
    user_id = message.from_user.id
    month_tasks = []
    user_tasks = todos.get(user_id, {})

    # Проверяем каждую дату в todos и добавляем задачи за указанный месяц
    for date, tasks in user_tasks.items():
        if date.split('.')[1] == month_number:
            month_tasks.extend(tasks)

    if month_tasks:
        tasks_text = "\n".join(f"{i + 1}. [ ] {task}" for i, task in enumerate(month_tasks, start=1))
        bot.send_message(user_id, f'Задачи за {get_month_name(month_number)}:\n{tasks_text}')
    else:
        bot.send_message(user_id, f'Задач за {get_month_name(month_number)} нет.')

    # Сбрасываем состояние пользователя
    user_states[user_id]['state'] = None


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


def show_all_tasks(message):
    all_tasks_text = ""
    for date, tasks in todos.items():
        all_tasks_text += f'Задачи на {date}:\n'
        all_tasks_text += "\n".join(f"[ ] {task}" for task in tasks)
        all_tasks_text += "\n\n"

    if all_tasks_text:
        bot.send_message(message.from_user.id, all_tasks_text)
    else:
        bot.send_message(message.from_user.id, "Задач пока нет.")

#----------------ClearTasks--------------------------


# Функция для очистки файла с задачами(Хотя ни хрена не понятно чьего файла какого пользователя задач...только своих чтоли тогда причем тут админ)
def clear_tasks():
    global todos
    print(todos)
    todos = {}
    save_todos(todos)
    print(todos)
    print ("Задачи только что добавленные очищены")
    return "Задачи только что добавленные очищены"



# Обработчик для кнопки очистки задач
@bot.message_handler(commands=['clear_tasks'])
def handle_clear_tasks(message):
    user_id = message.from_user.id
    # Устанавливаем состояние пользователя
    set_state(user_id, STATE_NONE)
    # Проверяем состояние пользователя (здесь нет необходимости вызывать get)
    if user_id in admin_list:
        result = clear_tasks()
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")


#---------------Delete--------------------------

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


#---------------ExitSave------------

# Функция для сохранения задач и access_list при выключении
def save_on_exit(todos, access_list):
    try:
        # Сохраняем todos
        save_todos(todos)
        print("Задачи сохранены в файл")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")



# Обработчик для команды /exitsave
@bot.message_handler(commands=['exitsave'])
def exit_program(message):
    save_on_exit(todos)

   # Сохраняем состояния todos
    save_todos(todos)
    print("Задачи  сохранены в файлы")

    # Отправляем сообщение о завершении работы бота
    bot.send_message(message.from_user.id, 'Спасибо за использование! Задачи добавлены. До свидания!')

    # Останавливаем бота
    bot.stop_polling()



# Регистрируем функцию save_on_exit для выполнения при завершении работы
atexit.register(save_on_exit, todos)



bot.polling(none_stop=True)