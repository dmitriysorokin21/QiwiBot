# IMPORTS
from config import *
from SimpleQIWI import *
from telebot import *
from time import *
# IMPORTS

bot = TeleBot(TOKEN)
wallet = QApi(token='', phone='')
tel = ''
summ = ''
comm = ''

# CLASS QIWI
class qiwi:
    def __init__(self, phone, token):
        self.phone = phone
        self.token = token
# CLASS QIWI


@bot.message_handler(commands=['start'])
def welcome(message):
    global wallet
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    watch_balance = types.KeyboardButton('💵 Посмотреть баланс 💵')
    send_money_button = types.KeyboardButton('💳 Перевести на кошелек 💳')
    edit_data = types.KeyboardButton('🖊️ Изменить данные 🖊️')
    markup.add(watch_balance)
    markup.add(send_money_button)
    markup.add(edit_data)
    bot.send_message(
        message.chat.id,
        'Привет, ' + message.from_user.first_name +
        '.\nЯ бот <b>QIWI</b>. \nС моей помощью ты можешь смотреть баланс кошелька, совершать переводы и смотреть историю. \nДля начала работы бота, заполни некоторые данные.',
        parse_mode='html')
    sleep(2)
    get_phone(message)
    
@bot.message_handler(commands=['edit'])
def get_phone(message):
    global wallet
    bot.send_message(message.chat.id,
                     '📞 Пришлите свой номер телефона\n\nНапример : +79999999999 📞')
    bot.register_next_step_handler(message, get_token)

def get_token(message):
    global wallet
    wallet.phone = message.text
    bot.send_message(
        message.chat.id,
        '🔐 Пришлите свой токен QIWI\n\nЕго можно взять <a href="https://qiwi.com/api">отсюда</a> 🔐',
        parse_mode='html',
        disable_web_page_preview=True)
    bot.register_next_step_handler(message, get_data)

def get_data(message):
    global wallet
    wallet.token = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    watch_balance = types.KeyboardButton('💵 Посмотреть баланс 💵')
    send_money_button = types.KeyboardButton('💳 Перевести на кошелек 💳')
    edit_data = types.KeyboardButton('🖊️ Изменить данные 🖊️')
    markup.add(watch_balance)
    markup.add(send_money_button)
    markup.add(edit_data)
    try:
        wallet = QApi(token=wallet.token, phone=wallet.phone)
        print(wallet.balance)
        bot.send_message(message.chat.id, '👌 Все готово к использованию бота! 👌', reply_markup=markup)
    except:
        bot.send_message(message.chat.id, '⚠️ Что-то пошло не так, попробуйте заполнить данные еще раз ⚠️')
        get_phone(message)

@bot.message_handler(regexp='💵 Посмотреть баланс 💵')
def balance(message):
    global wallet
    bot.send_message(message.chat.id, '💵 Ваш баланс : ' + str(wallet.balance[0]) + '₽ 💵')

@bot.message_handler(regexp='💳 Перевести на кошелек 💳')
def send_money_phone(message):
    bot.send_message(message.chat.id, '📞Пришлите номер кошелька QIWI, на который хотите отправить деньги\n\nНапример : +79999999999 📞')
    bot.register_next_step_handler(message, send_money_summ)
def send_money_summ(message):
    global tel
    tel = message.text
    try:
        len(tel) > 11
        bot.send_message(message.chat.id, '💵 Пришлите количество денег, которые хотите отправить (в рублях) 💵')
        bot.register_next_step_handler(message, send_money_comm)
    except:
        bot.send_message(message.chat.id, '⚠️ Введите правильный номер телефона\n\nНапример : +79999999999 ⚠️')
        send_money_phone(message)
def send_money_comm(message):
    global summ
    summ = message.text
    try:
        float(summ)
        keyboard = types.InlineKeyboardMarkup()
        key_send = types.InlineKeyboardButton(text='👌 Да, хочу 👌', callback_data='yes')
        keyboard.add(key_send)
        key_edit = types.InlineKeyboardButton(text='❌ Нет, спасибо ❌', callback_data='no')
        keyboard.add(key_edit)
        bot.send_message(message.chat.id, '📝 Хотите прислать комментарий к платежу? 📝', reply_markup=keyboard)
    except:
        bot.send_message(message.chat.id, '⚠️ Введите правильную сумму для перевода ⚠️')
        send_money_summ(message)

def abc123(message):
    bot.send_message(message.chat.id, '📝 Введите комментарий 📝')
    bot.register_next_step_handler(message, abc321)
def abc321(message):
    global tel
    global summ
    global comm
    global wallet
    comm = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_send = types.InlineKeyboardButton(text='👌 Да, уверен 👌', callback_data='yea1')
    keyboard.add(key_send)
    key_edit = types.InlineKeyboardButton(text='❌ Нет, не уверен ❌', callback_data='nope1')
    keyboard.add(key_edit)
    bot.send_message(message.chat.id, '❓ Вы уверены, что хотите отправить на номер ' + str(tel) + ' ' + str(summ) + '₽ с комментарием "' + str(comm) + '" ❓', reply_markup=keyboard)
    bot.register_next_step_handler(message, dhsdsd)
    

def nocomm(message):
    global wallet
    global summ
    global tel
    keyboard = types.InlineKeyboardMarkup()
    key_send = types.InlineKeyboardButton(text='👌 Да, уверен 👌', callback_data='yea2')
    keyboard.add(key_send)
    key_edit = types.InlineKeyboardButton(text='❌ Нет, не уверен ❌', callback_data='nope2')
    keyboard.add(key_edit)
    bot.send_message(message.chat.id, '❓ Вы уверены, что хотите отправить на номер ' + str(tel) + ' ' + str(summ) + '₽ без комментария '  + '❓', reply_markup=keyboard)
    bot.register_next_step_handler(message, fdfdf)
   # try:
   #     wallet.pay(account=tel, amount=summ, comment='')
   #     bot.send_message(message.chat.id, 'Платеж отправлен успешно!')
  #  except:
  #      bot.send_message(message.chat.id, '⚠️ Не удалось отправить платеж, проверьте правильность перевода ⚠️')
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'yes':
        abc123(call.message)
    elif call.data == 'no':
        nocomm(call.message)

@bot.callback_query_handler(func=lambda call: True)
def dhsdsd(call):
    global wallet
    global tel
    global summ
    global comm
    if call.data == 'yea1':
        try:
            wallet.pay(account=tel, amount=summ, comment=comm)
            bot.send_message(message.chat.id, '✔️ Платеж совершен успешно! ✔️')
        except:
            bot.send_message(message.chat.id, '⚠️ Не удалось совершить платеж ⚠️')

    elif call.data == 'nope1':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        watch_balance = types.KeyboardButton('💵 Посмотреть баланс 💵')
        send_money_button = types.KeyboardButton('💳 Перевести на кошелек 💳')
        edit_data = types.KeyboardButton('🖊️ Изменить данные 🖊️')
        markup.add(watch_balance)
        markup.add(send_money_button)
        markup.add(edit_data)
        bot.send_message(message.chat.id, '🤔 Выберите что делать 🤔', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def fdfdf(call):
    if call.data == 'yea2':
        global wallet
        global summ
        global tel
        try:
            wallet.pay(account=tel, amount=summ, comment='')
            bot.send_message(message.chat.id, '✔️ Платеж отправлен успешно! ✔️')
        except:
            bot.send_message(message.chat.id, '⚠️ Не удалось отправить платеж, проверьте правильность перевода ⚠️')
    elif call.data == 'nope2':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        watch_balance = types.KeyboardButton('💵 Посмотреть баланс 💵')
        send_money_button = types.KeyboardButton('💳 Перевести на кошелек 💳')
        edit_data = types.KeyboardButton('🖊️ Изменить данные 🖊️')
        markup.add(watch_balance)
        markup.add(send_money_button)
        markup.add(edit_data)
        bot.send_message(message.chat.id, 'Выберите что делать', reply_markup=markup)


bot.polling(none_stop=True)