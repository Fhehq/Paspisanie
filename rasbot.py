import telebot
from telebot import types
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.send_message(message.chat.id, 'Классное фото, но к сожалению я не умею принимать информацию с фото.')


@bot.message_handler(content_types=['video'])
def video(message):
    bot.send_message(message.chat.id, 'Классное  видео, но к сожалению я не умею принимать информацию с видео.')


# Команда для старта бота
@bot.message_handler(commands=["start"])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Четная', callback_data='chet')
    btn2 = types.InlineKeyboardButton('Не четная', callback_data='nchet')
    btn3 = types.InlineKeyboardButton('Звонки', callback_data='zvonki')
    markup.row(btn1, btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id,f'сап, {message.from_user.first_name}, чтобы посмотреть рассписание выбери неделю'
                     f'\nДля просмотра звоноков нажми на кнопку', reply_markup=markup)
    
#======================================= КНОПКА ГЛАВНОЕ МЕНЮ =========================================== 
#======================================= КНОПКА ГЛАВНОЕ МЕНЮ =========================================== 
#======================================= КНОПКА ГЛАВНОЕ МЕНЮ =========================================== 
@bot.callback_query_handler(func=lambda call: call.data == "start")
def handle_back_button(callback):
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
        monday = types.InlineKeyboardButton(text="Пон-к", callback_data="mon")
        Tuesdey = types.InlineKeyboardButton(text="Вторник", callback_data="tue")
        wednesday = types.InlineKeyboardButton(text="Среда", callback_data="wed")
        thursday = types.InlineKeyboardButton(text="Четверг", callback_data="thu")
        friday = types.InlineKeyboardButton(text="Пятница", callback_data="fri")    
        markup.row(monday, Tuesdey, wednesday, thursday, friday  )        
        markup.add(back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Вы выбрали четную неделю\nТеперь выберете день',
                              reply_markup=markup)
    elif call.data == 'nchet':
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text="Главное меню", callback_data="start")
        monday = types.InlineKeyboardButton(text="Пон-к", callback_data="nmon")
        Tuesdey = types.InlineKeyboardButton(text="Вторник", callback_data="ntue")
        wednesday = types.InlineKeyboardButton(text="Среда", callback_data="nwed")
        thursday = types.InlineKeyboardButton(text="Четверг", callback_data="nthu")
        friday = types.InlineKeyboardButton(text="Пятница", callback_data="nfri")    
        markup.row(monday, Tuesdey, wednesday, thursday, friday)        
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
    elif call.data == 'tue':
        markup = types.InlineKeyboardMarkup()
        day = types.InlineKeyboardButton(text="Выбор дня", callback_data="chet")
        next = types.InlineKeyboardButton(text="▶️", callback_data="wed")
        back = types.InlineKeyboardButton(text="◀️", callback_data="mon")        
        markup.add(back,day,next)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Вы выбрали Вторник чет. недели(Дистант):\n'
                                     '1: химия каб. 408\n'
                                     '2: проектный менеджмент каб. 407\n'
                                     '3: мдк разработка программного обеспечения каб. 305\n'
                                     '4: математика каб. 406' , reply_markup=markup)
    elif call.data == 'mon':
        markup = types.InlineKeyboardMarkup()
        day = types.InlineKeyboardButton(text="Выбор дня", callback_data="chet")
        next = types.InlineKeyboardButton(text="▶️", callback_data="tue")
        back = types.InlineKeyboardButton(text="◀️", callback_data="mon")        
        markup.add(back,day,next)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=f'Вы выбрали Понедельник чет. недели:\n'
                                            '1: разговоры о важном\n'
                                            '2: биология\n'
                                            '3: литература', reply_markup=markup)
#monday, Tuesdey, wednesday, thursday, friday


     

@bot.message_handler(func=lambda message: True)
def none(message):
    bot.send_message(message.chat.id, 'К сожалению я не умею читать текст:('
                                      '\n Введите команду которую я знаю.')


bot.polling(none_stop=True)