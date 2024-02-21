import telebot
from telebot import types

number = 0


def info(message, number):
    if number == 0:
        with open('./photo/one_time.jpeg', 'rb') as file:
            bot.send_photo(message.chat.id, file,
                           '<b>Мытьё окон, балконов, остеклений:</b>\n'
                           'Очистка и удаление загрязнений с поверхности стекла и других материалов,'
                           'используемых для оконных и балконных конструкций. Мытьё снаружи '
                           'и/или внутри.',
                           parse_mode='html')
            bot.send_message(message.chat.id, 'Учтите что заказ принимаются от 3.500 рублей.')
    elif number == 1:
        with open('./photo/supportibe.jpeg', 'rb') as file:
            bot.send_photo(message.chat.id, file,
                           '<b>Поддерживающая уборка:</b>\n'
                           'Направлена на поддержание чистоты и порядка в помещении, предотвращение '
                           'накопления грязи и пыли, а также сохранение красоты и ухоженности интерьера.',
                           parse_mode='html')
        bot.send_message(message.chat.id, 'Учтите что заказ принимаются от 3.500 рублей.')
    elif number == 2:
        with open('./photo/general.jpeg', 'rb') as file:
            bot.send_photo(message.chat.id, file,
                           '<b>Генеральная уборка:</b>\nТщательное очищение помещения. Её главная цель - полное '
                           'удаление пыли, грязи и загрязнений, устранение запахов, а также восстановление '
                           'чистоты и свежести помещения.', parse_mode='html')
        bot.send_message(message.chat.id, 'Учтите что заказ принимаются от 5.500 рублей.')
    elif number == 3:
        with open('./photo/repair.jpeg', 'rb') as file:
            bot.send_photo(message.chat.id, file,
                           '<b>Уборка после ремонта:</b>Глубокое очищение помещения от пыли, грязи, '
                           'следов цемента, клея, красок, растворителей и других строй. отходов. '
                           'Очищаются'
                           'буквально все места, от пола до потолка.', parse_mode='html')
        bot.send_message(message.chat.id, 'Учтите что заказ принимаются от 8.500 рублей.')
    elif number == 4:
        with open('./photo/emergency.jpeg', 'rb') as file:
            bot.send_photo(message.chat.id, file,
                           '<b>Уборка после ЧП:</b>\nПосле пожара, потопа, смерти, выброса канализации и пр.. '
                           'Частичное восстановление помещения, устранение запахов и его очага, удаление сажи '
                           'и копоти, и многое другое.', parse_mode='html')
        bot.send_message(message.chat.id, 'Учтите что заказ принимаются от 10.000 рублей.')
    elif number == 5:
        bot.send_message(message.chat.id,
                         '<b>Другое:</b>\n'
                         'Следует переговорить со специалистом', parse_mode='html')


def site(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://swift-cleaning.ru/'))
    bot.reply_to(message, 'Компания''\t"Swift Clining"', reply_markup=markup)


"""     CLICK       """


def yes_no_click(message):
    if message.text.lower() == 'да':
        square = bot.send_message(message.chat.id, 'Сколько квадратных метров?')
        bot.register_next_step_handler(square, summ)
    elif message.text.lower() == 'нет':
        cleaning(message)


def summ(message):
    if message.text.isdigit():
        square = int(message.text)
        if number == 0:
            summa = square * 1200
            bot.send_message(message.chat.id, 'Примерная сумма составила: {:,} рублей'.format(summa))
    else:
        bot.send_message(message.chat.id, 'n/a')


def on_click(message):
    message_command = ['Перейти на сайт 💻', 'Заказать уборку 🧹', 'Оставить отзыв 📖', 'Помощь ⚙️']
    if message.text == message_command[1]:
        cleaning(message)
    elif message.text == message_command[0]:
        site(message)
    elif message.text == message_command[2]:
        bot.send_message(message.chat.id, 'На доработке')
    elif message.text == message_command[3]:
        bot.send_message(message.chat.id, 'На доработке')


def on_cleaning_click(message):
    global number
    command_choice = ['Разовый клининг', 'Поддерживающая уборка', 'Генеральная уборка', 'Уборка после ремонта',
                      'Уборка после ЧП', 'Другое']
    if message.text == command_choice[0]:
        number = 0
        info(message, number)
        yes_no(message)
    elif message.text == command_choice[1]:
        number = 1
        info(message, number)
        yes_no(message)
    elif message.text == command_choice[2]:
        number = 2
        info(message, number)
        yes_no(message)
    elif message.text == command_choice[3]:
        number = 3
        info(message, number)
        yes_no(message)
    elif message.text == command_choice[4]:
        number = 4
        info(message, number)
        yes_no(message)
    elif message.text == command_choice[5]:
        number = 5
        info(message, number)
        yes_no(message)


"""   ДОБАВЛЕНИЕ КНОПОК   """


def yes_no(message):
    button = types.ReplyKeyboardMarkup()
    button_yes = types.InlineKeyboardButton('Да')
    button_no = types.InlineKeyboardButton('Нет')
    button.add(button_yes)
    button.add(button_no)
    bot.send_message(message.chat.id, 'Подходит такая уборка?', reply_markup=button)
    bot.register_next_step_handler(message, yes_no_click)


def cleaning(message):
    button = types.ReplyKeyboardMarkup()
    one_time = types.InlineKeyboardButton('Разовый клининг')
    supportive = types.InlineKeyboardButton('Поддерживающая уборка')
    button.row(one_time, supportive)
    general = types.InlineKeyboardButton('Генеральная уборка')
    button.row(general)
    repair = types.InlineKeyboardButton('Уборка после ремонта')
    emergency = types.InlineKeyboardButton('Уборка после ЧП')
    button.row(repair, emergency)
    other = types.InlineKeyboardButton('Другое')
    button.row(other)
    bot.send_message(message.chat.id, 'Выберите вариант уборки', reply_markup=button)
    bot.register_next_step_handler(message, on_cleaning_click)


if __name__ == '__main__':
    bot = telebot.TeleBot('6916933008:AAH8ayE-T40zuKnMKQzfVk_jeVNWr047ins')


    @bot.message_handler(commands=['start'])
    def start_main(message):
        markup = types.ReplyKeyboardMarkup()
        site_button = types.InlineKeyboardButton('Перейти на сайт 💻')
        order_cleaning = types.InlineKeyboardButton('Заказать уборку 🧹')
        review_button = types.InlineKeyboardButton('Оставить отзыв 📖')
        help_button = types.InlineKeyboardButton('Помощь ⚙️')
        command = [order_cleaning, site_button, review_button, help_button]
        for i_command in command:
            markup.add(i_command)
        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}. Буду рад помочь вам!',
                         reply_markup=markup)
        bot.register_next_step_handler(message, on_click)


    @bot.message_handler(commands=['help'])
    def help_main(message):
        bot.send_message(message.chat.id, '<b>Help information</b>'' :\n Артем крутой 123', parse_mode='html')


    @bot.message_handler()
    def echo(message):
        message_user = ['привет', 'здравствуйте', 'салам', 'хай']
        if message.text.lower() in message_user:
            bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}. Буду рад помочь вам!')
        else:
            bot.send_message(message.chat.id, f'Я вас не понимаю. Попробуйте ещё раз!')


    bot.polling(none_stop=True)
