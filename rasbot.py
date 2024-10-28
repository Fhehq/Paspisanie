import telebot
from telebot import types
import os
from dotenv import load_dotenv, find_dotenv
import json
load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('TOKEN'))
SCHEDULE_FILE = 'schedule.json'
USERS_FILE = 'users.data'

    

#==========================РАСПИСАНИЕ==========================
def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Если файла нет, возвращаем расписание по умолчанию
        return {
            'mon': ['1: разговоры о важном', '2: биология', '3: литература'],
            'tue': ['1: химия 408', '2: проектный менеджмент 407', '3: мдк разработка программного обеспечения305']
                }
        
# Функция сохранения расписания в файл
def save_schedule():
    with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=4)
        
# Загружаем расписание при запуске
schedule = load_schedule()       
        #====СМЕНА РАСПИСНИЯ====    
@bot.callback_query_handler(func=lambda call: call.data == 'raspis')
def change_schedule(callback):
    markup = types.InlineKeyboardMarkup() 
    days = [
        ('Понедельник чет', 'mon'),
        ('Вторник чет', 'tue'),
        ('Среда чет', 'wed'),
        ('Четверг чет', 'thu'),
        ('Пятница чет', 'fri'),
        ('Понедельник не чет', 'nmon'),
        ('Вторник не чет', 'ntue'),
        ('Среда не чет', 'nwed'),
        ('Четверг не чет', 'nthu'),
        ('Пятница не чет', 'nfri')
            ]
    for day_name, day_code in days:
        button = types.InlineKeyboardButton(text=day_name, callback_data=f'edit_{day_code}')
        adm = types.InlineKeyboardButton(text='Назад', callback_data="admpan")
        markup.add(button)
        markup.row(adm)
        
    
    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                          text='Выберите день для изменения расписания:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_'))
def edit_day_schedule(callback):
    day = callback.data.split('_')[1]  # Получаем день недели из callback_data
    current_schedule = '\n'.join(schedule[day])  # Текущее расписание

    bot.send_message(callback.message.chat.id, 
                     f'Текущее расписание на {day}:\n{current_schedule}\n\n'
                     'Отправьте новое расписание (каждый предмет с новой строки).')

    bot.register_next_step_handler(callback.message, process_new_schedule, day)

def process_new_schedule(message, day):
    new_schedule = message.text.split('\n')
    schedule[day] = new_schedule  # Обновляем расписание
    save_schedule()  # Сохраняем обновленное расписание в файл

    bot.send_message(message.chat.id, f'Расписание на {day} обновлено.')


#==========================РАСПИСАНИЕ==========================


#===========================АДМИН ПАНЕЛЬ=======================
#===========================АДМИН ПАНЕЛЬ=======================
#===========================АДМИН ПАНЕЛЬ=======================
def get_admins():
  try:
    with open('admins.txt', 'r') as f:
      admin_ids = [int(line.strip()) for line in f]
    return admin_ids
  except FileNotFoundError:
    return []

def save_admins(admin_ids):
  with open('admins.txt', 'w') as f:
    for admin_id in admin_ids:
      f.write(str(admin_id) + '\n')

admin_ids = get_admins() 

def is_admin(message):
  return message.from_user.id in admin_ids


@bot.message_handler(commands=['admin'])
def admin_menu(message):
  if is_admin(message):
    markup = types.InlineKeyboardMarkup()
    adm1 = types.InlineKeyboardButton("Админ панель", callback_data="admpan")
    markup.add(adm1)
    bot.send_message(message.chat.id, f"Здраствйте Администратор, {message.from_user.first_name} ",
             reply_markup=markup)
  else:
    bot.send_message(message.chat.id, 'У вас нет прав доступа.')


@bot.callback_query_handler(func=lambda call: call.data == "admpan")
def handle_back_button(callback):
  markup = types.InlineKeyboardMarkup()
  menu = types.InlineKeyboardButton(text="Главное меню", callback_data="start")
  admadd = types.InlineKeyboardButton(text="Добавить Админа", callback_data="admin_add")
  admdel = types.InlineKeyboardButton(text="Удалить Админа", callback_data="delete_admin")
  item = types.InlineKeyboardButton(text='Изменить Расписание', callback_data='raspis')
  spam_button = types.InlineKeyboardButton(text='Рассылка', callback_data='send_spam')  
  user_count_button = types.InlineKeyboardButton(text='Количество пользователей', callback_data='user_count')
  markup.row(admadd, admdel)
  markup.row(item, spam_button)
  markup.row(user_count_button)
  markup.add(menu)
  bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
             text=f'Выберите что хотите сделать', reply_markup=markup)
  
  
@bot.callback_query_handler(func=lambda call: call.data == "user_count")
def show_user_count(callback):
    markup = types.InlineKeyboardMarkup()
    adm12 = types.InlineKeyboardButton("Назад", callback_data="admpan")
    adm13 = types.InlineKeyboardButton("Их ID", callback_data="idusers")
    markup.row(adm12)
    markup.add(adm13)
    users = get_users()
    user_count = len(users)
    bot.send_message(callback.message.chat.id, f"Количество пользователей: {user_count}", reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: call.data == "idusers")
def show_user_count(callback):
    markup = types.InlineKeyboardMarkup()
    adm12 = types.InlineKeyboardButton("Назад", callback_data="user_count")
    markup.add(adm12)
    users = get_users()
    user_count =users
    bot.send_message(callback.message.chat.id, f"Их ID:\n{user_count}", reply_markup=markup)

# ----------------ДОБАВЛЕНИЕ АДМИМНА-----------  
# ----------------ДОБАВЛЕНИЕ АДМИМНА-----------
@bot.callback_query_handler(func=lambda call: call.data == "admin_add")
def add_admin(call):
  markup = types.InlineKeyboardMarkup()
  adm12 = types.InlineKeyboardButton("Назад", callback_data="admpan")
  markup.add(adm12)
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
             text="Введите ID нового администратора:", reply_markup=markup)
  bot.register_next_step_handler(call.message, process_new_admin_id)


def process_new_admin_id(message):
  global admin_ids
  new_id = message.text.strip()
  try:
    new_id = int(new_id)
    admin_ids.append(new_id)
    save_admins(admin_ids) # Сохраняем ID в файл
    bot.send_message(message.chat.id, f"ID {new_id} добавлен в список администраторов.")
  except ValueError:
    bot.send_message(message.chat.id, "Введите корректный ID.") #

# ----------------ДОБАВЛЕНИЕ АДМИМНА-----------
# ----------------ДОБАВЛЕНИЕ АДМИМНА-----------
# ----------------УДАЛЕНИЕ АДМИМНА-------------
# ----------------УДАЛЕНИЕ АДМИМНА-------------
@bot.callback_query_handler(func=lambda call: call.data == "delete_admin")
def delete_admin(call):
  markup = types.InlineKeyboardMarkup()
  adm12 = types.InlineKeyboardButton("Назад", callback_data="admpan")
  markup.add(adm12)
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
             text=f"Введите ID администратора, которого нужно удалить:\n{admin_ids}", reply_markup=markup)
  bot.register_next_step_handler(call.message, process_delete_admin_id)


def process_delete_admin_id(message):
  global admin_ids
  try:
    id_to_delete = int(message.text)
    if id_to_delete == 1086906276:
      bot.send_message(message.chat.id, f"ID {id_to_delete} Нельзя удалить.")
    elif id_to_delete in admin_ids:
      admin_ids.remove(id_to_delete)
      save_admins(admin_ids)
      bot.send_message(message.chat.id, f"ID {id_to_delete} удален из списка администраторов.")

    else:
      bot.send_message(message.chat.id, f"ID {id_to_delete} не найден в списке администраторов.")
  except ValueError:
    bot.send_message(message.chat.id, "Введите корректный ID.")

# ----------------УДАЛЕНИЕ АДМИМНА-------------
# ----------------УДАЛЕНИЕ АДМИМНА-------------
#======СПАМ=====СПАМ=====СПАМ======СПАМ=======СПАМ
#======СПАМ=====СПАМ=====СПАМ======СПАМ=======СПАМ
#======СПАМ=====СПАМ=====СПАМ======СПАМ=======СПАМ
@bot.callback_query_handler(func=lambda call: call.data == "send_spam")
def send_spam(callback):
    global is_spam_cancelled
    is_spam_cancelled = False  # Сбрасываем статус отмены перед началом новой рассылки
    
    markup = types.InlineKeyboardMarkup()
    cancel_button = types.InlineKeyboardButton("Отменить рассылку", callback_data="cancel_spam")
    markup.add(cancel_button)
    
    msg = bot.send_message(callback.message.chat.id, "Введите текст для рассылки:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_spam_text)

@bot.callback_query_handler(func=lambda call: call.data == "cancel_spam")
def cancel_spam(call):
    global is_spam_cancelled
    is_spam_cancelled = True  # Устанавливаем флаг отмены рассылки
    markup = types.InlineKeyboardMarkup()
    admmen = types.InlineKeyboardButton("Админ Меню", callback_data="admpan")
    markup.add(admmen)
    bot.send_message(call.message.chat.id, "Рассылка отменена.", reply_markup=markup)

def process_spam_text(message):
    global is_spam_cancelled
    
    spam_text = message.text
    if spam_text:
        users = get_users()
        for user_id in users:
            if is_spam_cancelled:
                markup = types.InlineKeyboardMarkup()
                admmen = types.InlineKeyboardButton("Админ Меню", callback_data="admpan")
                markup.add(admmen)
                bot.send_message(message.chat.id, "Рассылка была отменена.", reply_markup=markup)
                break  # Прекращаем рассылку при отмене
            try:
                bot.send_message(user_id, spam_text)
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
        else:
            if not is_spam_cancelled:
                bot.send_message(message.chat.id, "Рассылка завершена.")
    else:
        bot.send_message(message.chat.id, "Сообщение не может быть пустым.")
#======СПАМ=====СПАМ=====СПАМ======СПАМ=======СПАМ
#======СПАМ=====СПАМ=====СПАМ======СПАМ=======СПАМ
#======СПАМ=====СПАМ=====СПАМ======СПАМ=======СПАМ
#===========================АДМИН ПАНЕЛЬ=======================
#===========================АДМИН ПАНЕЛЬ=======================
#===========================АДМИН ПАНЕЛЬ=======================



  
@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.send_message(message.chat.id, 'Классное фото, но к сожалению я не умею принимать информацию с фото.')


@bot.message_handler(content_types=['video'])
def video(message):
    bot.send_message(message.chat.id, 'Классное  видео, но к сожалению я не умею принимать информацию с видео.')


# Команда для старта бота
@bot.message_handler(commands=["start"])
def main(message):
    users = get_users()  # Получаем текущих пользователей из переменной окружения
    if message.chat.id not in users:
        users.add(message.chat.id)  # Добавляем нового пользователя
        save_users(users)  # Сохраняем обновлённый список пользователей


    
    # Остальной код для отображения кнопок и работы с расписанием
    if is_admin(message):
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Четная', callback_data='chet')
        btn2 = types.InlineKeyboardButton('Не четная', callback_data='nchet')
        btn3 = types.InlineKeyboardButton('Звонки', callback_data='zvonki')
        adm = types.InlineKeyboardButton("Админ панель", callback_data="admpan")
        markup.row(btn1, btn2, btn3)
        markup.add(adm)
        bot.send_message(message.chat.id, f'Сап, {message.from_user.first_name}, чтобы посмотреть расписание, выбери неделю\n'
                                          f'Для просмотра звонков нажми на кнопку', reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Четная', callback_data='chet')
        btn2 = types.InlineKeyboardButton('Не четная', callback_data='nchet')
        btn3 = types.InlineKeyboardButton('Звонки', callback_data='zvonki')
        markup.row(btn1, btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id, f'Сап, {message.from_user.first_name}, чтобы посмотреть расписание, выбери неделю\n'
                                          f'Для просмотра звонков нажми на кнопку', reply_markup=markup)

def get_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f))  # Загружаем данные и конвертируем в множество
    return set()  # Если файла нет, возвращаем пустое множество

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(users), f, ensure_ascii=False, indent=4)  # Преобразуем множество в список перед сохранением
    

@bot.message_handler(func=lambda message: True)
def track_users(message):
    users = get_users()
    if message.chat.id not in users:
        users.add(message.chat.id)
        save_users(users) 
#======================================= КНОПКА ГЛАВНОЕ МЕНЮ =========================================== 
#======================================= КНОПКА ГЛАВНОЕ МЕНЮ =========================================== 
#======================================= КНОПКА ГЛАВНОЕ МЕНЮ =========================================== 
@bot.callback_query_handler(func=lambda call: call.data == "start")
def handle_back_button(callback):
    if is_admin(callback.message):
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Четная', callback_data='chet')
        btn2 = types.InlineKeyboardButton('Не четная', callback_data='nchet')
        btn3 = types.InlineKeyboardButton('Звонки', callback_data='zvonki')
        adm = types.InlineKeyboardButton("Админ панель", callback_data="admpan")
        markup.row(btn1, btn2, btn3)
        markup.add(adm)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                          text=f'сап, {callback.from_user.first_name}, чтобы посмотреть рассписание выбери неделю'
                                '\nДля просмотра звоноков нажми на кнопку', reply_markup=markup)
    else:    
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Четная', callback_data='chet')
        btn2 = types.InlineKeyboardButton('Не четная', callback_data='nchet')
        btn3 = types.InlineKeyboardButton('Звонки', callback_data='zvonki')
        markup.row(btn1, btn2)
        markup.add(btn3)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                            text=f'сап, {callback.from_user.first_name}, чтобы посмотреть рассписание выбери неделю'
                                  '\nДля просмотра звоноков нажми на кнопку', reply_markup=markup)


    

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
#=======================================  ЧЕТНАЯ ИЛИ НЕ ЧЕТНАЯ И ЗВОНКИ  =========================================== 
#=======================================  ЧЕТНАЯ ИЛИ НЕ ЧЕТНАЯ И ЗВОНКИ  =========================================== 
#=======================================  ЧЕТНАЯ ИЛИ НЕ ЧЕТНАЯ И ЗВОНКИ  =========================================== 
    if call.data == 'chet':
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text="Главное меню", callback_data="start")
        monday = types.InlineKeyboardButton(text="Понедельник", callback_data="mon")
        Tuesdey = types.InlineKeyboardButton(text="Вторник", callback_data="tue")
        wednesday = types.InlineKeyboardButton(text="Среда", callback_data="wed")
        thursday = types.InlineKeyboardButton(text="Четверг", callback_data="thu")
        friday = types.InlineKeyboardButton(text="Пятница", callback_data="fri")    
        markup.row(monday, Tuesdey)  
        markup.row(wednesday, thursday, friday)         
        markup.add(back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Вы выбрали четную неделю\nТеперь выберете день',
                              reply_markup=markup)
    elif call.data == 'nchet':
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text="Главное меню", callback_data="start")
        monday = types.InlineKeyboardButton(text="Понедельник", callback_data="nmon")
        Tuesdey = types.InlineKeyboardButton(text="Вторник", callback_data="ntue")
        wednesday = types.InlineKeyboardButton(text="Среда", callback_data="nwed")
        thursday = types.InlineKeyboardButton(text="Четверг", callback_data="nthu")
        friday = types.InlineKeyboardButton(text="Пятница", callback_data="nfri")    
        markup.row(monday, Tuesdey)
        markup.row(wednesday, thursday, friday)        
        markup.add(back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Вы выбрали не четную неделю\nТеперь выберете день',
                              reply_markup=markup)


    elif call.data == 'zvonki':
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text="Главное меню", callback_data="start")
        markup.add(back)
        bot.edit_message_text(chat_id=call.message.chat.id, text="Звонки:\nпонедельник (дистант):\n"
                                "классный час (разговоры о важном): 8:30-9:15\n"
                                "1 пара: 9:20-10:05 10:10-10:5\n"
                                "2 пара: 11-15-12:00; 12:05-12:50\n"
                                "3 пара: 13:20-14:05; 14:10-14:55\n"
                                "4 пара: 15:15-16:00; 16:05-16:50\n\n"
                                "Остальные дни\n"
                                "1 пара: 8:30-9:15; 9:20-10:05\n"
                                "2 пара: 10:25-11:10; 11:15-12:00\n"
                                "3 пара: 12:30-13:15; 13:20-14:05\n"
                                "4 пара: 14:25-15:10; 15:15-16:00\n", message_id=call.message.id, reply_markup=markup)

            
        
#=======================================  ЧЕТНАЯ ===========================================
#=======================================  ЧЕТНАЯ =========================================== 
#=======================================  ЧЕТНАЯ ===========================================                                    

    elif call.data == 'mon':
        day = 'mon'
        current_schedule = '\n'.join(schedule[day])

        markup = types.InlineKeyboardMarkup()
        day_button = types.InlineKeyboardButton(text="Выбор дня", callback_data="chet")
        next_button = types.InlineKeyboardButton(text="▶️", callback_data="tue")
        back_button = types.InlineKeyboardButton(text="◀️", callback_data="mon")        
        markup.add(back_button, day_button, next_button)

        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.id,
                            text=f'Вы выбрали Понедельник:\n{current_schedule}', 
                            reply_markup=markup)
    elif call.data == 'tue':
        day = 'tue'
        current_schedule = '\n'.join(schedule[day])

        markup = types.InlineKeyboardMarkup()
        day_button = types.InlineKeyboardButton(text="Выбор дня", callback_data="chet")
        next_button = types.InlineKeyboardButton(text="▶️", callback_data="wed")
        back_button = types.InlineKeyboardButton(text="◀️", callback_data="mon")        
        markup.add(back_button, day_button, next_button)

        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.id,
                            text=f'Вы выбрали Вторник:\n{current_schedule}', 
                            reply_markup=markup)
    elif call.data == 'wed':
        day = 'wed'
        current_schedule = '\n'.join(schedule[day])

        markup = types.InlineKeyboardMarkup()
        day_button = types.InlineKeyboardButton(text="Выбор дня", callback_data="chet")
        next_button = types.InlineKeyboardButton(text="▶️", callback_data="thu")
        back_button = types.InlineKeyboardButton(text="◀️", callback_data="tue")        
        markup.add(back_button, day_button, next_button)

        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.id,
                            text=f'Вы выбрали Среду:\n{current_schedule}', 
                            reply_markup=markup)
    elif call.data == 'thu':
        day = 'thu'
        current_schedule = '\n'.join(schedule[day])

        markup = types.InlineKeyboardMarkup()
        day_button = types.InlineKeyboardButton(text="Выбор дня", callback_data="chet")
        next_button = types.InlineKeyboardButton(text="▶️", callback_data="fri")
        back_button = types.InlineKeyboardButton(text="◀️", callback_data="wed")        
        markup.add(back_button, day_button, next_button)

        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.id,
                            text=f'Вы выбрали Четверг:\n{current_schedule}', 
                            reply_markup=markup)
    elif call.data == 'fri':
        day = 'fri'
        current_schedule = '\n'.join(schedule[day])

        markup = types.InlineKeyboardMarkup()
        day_button = types.InlineKeyboardButton(text="Выбор дня", callback_data="chet")
        next_button = types.InlineKeyboardButton(text="▶️", callback_data="fri")
        back_button = types.InlineKeyboardButton(text="◀️", callback_data="tue")        
        markup.add(back_button, day_button, next_button)

        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.id,
                            text=f'Вы выбрали Пятницу:\n{current_schedule}', 
                            reply_markup=markup)
#=======================================НЕ  ЧЕТНАЯ ===========================================
#=======================================НЕ  ЧЕТНАЯ =========================================== 
#=======================================НЕ  ЧЕТНАЯ ===========================================          
    elif call.data == 'nmon':
        day = 'nmon'
        current_schedule = '\n'.join(schedule[day])

        markup = types.InlineKeyboardMarkup()
        day_button = types.InlineKeyboardButton(text="Выбор дня", callback_data="nchet")
        next_button = types.InlineKeyboardButton(text="▶️", callback_data="ntue")
        back_button = types.InlineKeyboardButton(text="◀️", callback_data="nmon")        
        markup.add(back_button, day_button, next_button)

        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.id,
                            text=f'Вы выбрали Понедельник:\n{current_schedule}', 
                            reply_markup=markup)
    elif call.data == 'ntue':
        day = 'ntue'
        current_schedule = '\n'.join(schedule[day])

        markup = types.InlineKeyboardMarkup()
        day_button = types.InlineKeyboardButton(text="Выбор дня", callback_data="nchet")
        next_button = types.InlineKeyboardButton(text="▶️", callback_data="nwed")
        back_button = types.InlineKeyboardButton(text="◀️", callback_data="nmon")        
        markup.add(back_button, day_button, next_button)

        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.id,
                            text=f'Вы выбрали Вторник:\n{current_schedule}', 
                            reply_markup=markup)
    elif call.data == 'nwed':
        day = 'nwed'
        current_schedule = '\n'.join(schedule[day])

        markup = types.InlineKeyboardMarkup()
        day_button = types.InlineKeyboardButton(text="Выбор дня", callback_data="nchet")
        next_button = types.InlineKeyboardButton(text="▶️", callback_data="nthu")
        back_button = types.InlineKeyboardButton(text="◀️", callback_data="ntue")        
        markup.add(back_button, day_button, next_button)

        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.id,
                            text=f'Вы выбрали Среду:\n{current_schedule}', 
                            reply_markup=markup)
    elif call.data == 'nthu':
        day = 'nthu'
        current_schedule = '\n'.join(schedule[day])

        markup = types.InlineKeyboardMarkup()
        day_button = types.InlineKeyboardButton(text="Выбор дня", callback_data="nchet")
        next_button = types.InlineKeyboardButton(text="▶️", callback_data="nfri")
        back_button = types.InlineKeyboardButton(text="◀️", callback_data="nwed")        
        markup.add(back_button, day_button, next_button)

        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.id,
                            text=f'Вы выбрали Четверг:\n{current_schedule}', 
                            reply_markup=markup)
    elif call.data == 'nfri':
        day = 'nfri'
        current_schedule = '\n'.join(schedule[day])

        markup = types.InlineKeyboardMarkup()
        day_button = types.InlineKeyboardButton(text="Выбор дня", callback_data="nchet")
        next_button = types.InlineKeyboardButton(text="▶️", callback_data="nfri")
        back_button = types.InlineKeyboardButton(text="◀️", callback_data="ntue")        
        markup.add(back_button, day_button, next_button)

        bot.edit_message_text(chat_id=call.message.chat.id, 
                            message_id=call.message.id,
                            text=f'Вы выбрали Пятницу:\n{current_schedule}', 
                            reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def none(message):
    bot.send_message(message.chat.id, 'К сожалению я не умею читать текст:('
                                      '\n Введите команду которую я знаю.')


bot.polling(none_stop=True)