import telebot
from telebot import types
from search_site import title_url, start_search_site
import smtplib
from price_bid import amount_of_slaughter
from data import password, url_site, email_sender, email_getter
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from counter import counter
import re


def info(message, number_info):
    if number_info == 0:
        with open('./photo/one_time.jpeg', 'rb') as file:
            bot.send_photo(message.chat.id, file,
                           f'<b>{title_url["service"][number_info][0]}:</b>\n'
                           f'{title_url["service"][number_info][1]}', parse_mode='html')
            bot.send_message(message.chat.id, 'Учтите что заказ принимаются от {:,} рублей.'
                             .format(title_url["price"][number_info]))
    elif number_info == 1:
        with open('./photo/supportibe.jpeg', 'rb') as file:
            bot.send_photo(message.chat.id, file,
                           f'<b>{title_url["service"][number_info][0]}:</b>\n'
                           f'{title_url["service"][number_info][1]}', parse_mode='html')
        bot.send_message(message.chat.id, 'Учтите что заказ принимаются от {:,} рублей.'
                         .format(title_url["price"][number_info]))
    elif number_info == 2:
        with open('./photo/general.jpeg', 'rb') as file:
            bot.send_photo(message.chat.id, file,
                           f'<b>{title_url["service"][number_info][0]}:</b>\n'
                           f'{title_url["service"][number_info][1]}', parse_mode='html')
        bot.send_message(message.chat.id, 'Учтите что заказ принимаются от {:,} рублей.'.
                         format(title_url["price"][number_info]))
    elif number_info == 3:
        with open('./photo/repair.jpeg', 'rb') as file:
            bot.send_photo(message.chat.id, file,
                           f'<b>{title_url["service"][number_info][0]}:</b>\n'
                           f'{title_url["service"][number_info][1]}', parse_mode='html')
        bot.send_message(message.chat.id, 'Учтите что заказ принимаются от {:,} рублей.'
                         .format(title_url["price"][number_info]))
    elif number_info == 4:
        with open('./photo/emergency.jpeg', 'rb') as file:
            bot.send_photo(message.chat.id, file,
                           f'<b>{title_url["service"][number_info][0]}:</b>\n'
                           f'{title_url["service"][number_info][1]}', parse_mode='html')
        bot.send_message(message.chat.id, 'Учтите что заказ принимаются от {:,} рублей.'
                         .format(title_url["price"][number_info]))
    elif number_info == 5:
        bot.send_message(message.chat.id,
                         '<b>Другое:</b>\n'
                         'Следует переговорить со специалистом', parse_mode='html')


""" MESSAGE TELEGRAM IN EMAIL  """


def send_email(message, orders):
    mess = (f"Новая заявка:\n\nВид услуги: {orders['Type_of_cleaning']}\nИмя: {orders['Name']}\n"
            f"Телефон: {orders['Number']}\n Площадь m2:{orders['Square']}\n" + "Примерная сумма составила: {:,} рублей"
            .format(orders['Summa']))
    bot.send_message(message.chat.id, mess)
    msg = MIMEMultipart()
    msg["Subject"] = f'Telegram Заявка №{counter()}'
    msg.attach(MIMEText(mess + '\nlogin telegram: @{}'.format(message.from_user.username)))
    server = smtplib.SMTP("smtp.mail.ru", 587)
    server.starttls()

    server.login(email_sender, password)
    server.sendmail(email_sender, email_getter, msg.as_string())
    bot.send_message(message.chat.id, 'Спасибо, за ваше доверие!\nМенеджер свяжется с вами в течение 15 минут.')
    home_page(message)


"""   SITE    """


def site(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url=url_site))
    with open('./photo/logo.jpg', 'rb') as file:
        bot.send_photo(message.chat.id, file, 'Компания''\t<b>"Swift Cleaning</b>"',
                       reply_markup=markup, parse_mode='HTML')
    home_page(message)

"""  REVIEW SITE  """

def review_site(message):
    url = 'https://yandex.ru/maps/org/svift_klining/182540269027/?ll=82.978281%2C55.044315&z=13'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url=url))
    with open('./photo/logo2.jpg', 'rb') as file:
        bot.send_photo(message.chat.id, file, 'Благодарим вас, за ваше доверие к нам!"\nБудем благодарны если'
                                              ' оставите отзыв!', reply_markup=markup)
    home_page(message)


""" SUMMA CHECK """


def summ(message, number, choice):
    if message.text.isdigit():
        summa = 0
        square = int(message.text)
        if number == 0:
            summa = square * amount_of_slaughter["Мытьё окон, балконов"]
        elif number == 1:
            summa = square * amount_of_slaughter["Поддерживающая уборка"]
        elif number == 2:
            summa = square * amount_of_slaughter["Генеральная уборка"]
        elif number == 3:
            summa = square * amount_of_slaughter["Уборка после ремонта"]
        elif number == 4:
            summa = square * amount_of_slaughter["Уборка после ЧП"]
        if title_url['price'][number] < summa:
            bot.send_message(message.chat.id, 'Примерная сумма составила: <b>{:,}</b> рублей.'.format(summa),
                             parse_mode='html')
            summary_buttons(message, number, summa, square, choice)
        else:
            bot.send_message(message.chat.id, 'Извините минимальный заказ от <b>{:,}</b> рублей.\n'
                                              'Ваша сумма составила <b>{:,}</b> рублей.'
                             .format(title_url['price'][number], summa), parse_mode='html')
            yes_no_click(message, number, choice)
    else:
        bot.send_message(message.chat.id, 'Ошибка, введите площадь в цифрах.')
        yes_no_click(message, number, choice)


"""     CLICK       """


def yes_no_click(message, number, choice):
    if message.text.lower() == 'да':
        if number == 0:
            sash = bot.send_message(message.chat.id, 'Сколько оконных створок?')
            bot.register_next_step_handler(sash, summ, number, choice)
        else:
            square_m2 = bot.send_message(message.chat.id, 'Сколько квадратных метров?')
            bot.register_next_step_handler(square_m2, summ, number, choice)
    elif message.text.lower() == 'нет':
        cleaning(message)
    else:
        yes_no(message, number, choice)


def on_click(message):
    message_command = ['Перейти на сайт 💻', 'Заказать уборку 🧹', 'Оставить отзыв 📖', 'Информация ℹ️']
    if message.text == message_command[1]:
        cleaning(message)
    elif message.text == message_command[0]:
        site(message)
    elif message.text == message_command[2]:
        review_site(message)
    elif message.text == message_command[3]:
        info_in_company(message)
        home_page(message)
    else:
        bot.send_message(message.chat.id, 'Произошла ошибка ввода, повторите ещё раз')
        home_page(message)

def specialist(message):
    bot.send_message(message.chat.id,f'Специалист: {title_url["company"][0][1]}')

def on_cleaning_click(message):
    command_choice = ['Мытьё окон, балконов', 'Поддерживающая уборка', 'Генеральная уборка', 'Уборка после ремонта',
                      'Уборка после ЧП', 'Другое', 'Вернуться назад']
    if message.text == command_choice[0]:
        number = 0
        info(message, number)
        yes_no(message, number, command_choice[0])
    elif message.text == command_choice[1]:
        number = 1
        info(message, number)
        yes_no(message, number, command_choice[1])
    elif message.text == command_choice[2]:
        number = 2
        info(message, number)
        yes_no(message, number, command_choice[2])
    elif message.text == command_choice[3]:
        number = 3
        info(message, number)
        yes_no(message, number, command_choice[3])
    elif message.text == command_choice[4]:
        number = 4
        info(message, number)
        yes_no(message, number, command_choice[4])
    elif message.text == command_choice[5]:
        number = 5
        info(message, number)
        specialist(message)
        cleaning(message)
    elif message.text == command_choice[6]:
        home_page(message)
    else:
        bot.send_message(message.chat.id, 'Произошла ошибка ввода, повторите ещё раз')
        cleaning(message)

"""  DICTIONARY ORDER  """

def list_order(message, number, summa, square, choice, phone, name, orders):
    orders['Number'] = phone
    orders['Name'] = name
    orders['Type_of_cleaning'] = choice
    orders['Summa'] = summa
    orders['Square'] = square


"""    ORDER   """


def order(message, number, summa, square, choice):
    orders = {}
    name_phone = message.text.split()
    if message.text == 'Вернуться назад':
        decor(message, number, summa, square, choice)
    elif len(name_phone) == 2:
        name = name_phone[0]
        phone = name_phone[1]
        if (phone.isdigit()) and (len(phone) == 11) and ((phone[0] == '7') or (phone[0] == '8')):
            list_order(message, number, summa, square, choice, phone, name, orders)
            send_email(message, orders)
        else:
            bot.send_message(message.chat.id, 'Номер введен неверно, попробуйте снова')
            decor(message, number, summa, square, choice)
    elif message.text == 'Вернуться назад':
        decor(message, number, summa, square, choice)
    else:
        bot.send_message(message.chat.id, 'Ошибка ввода, попробуйте снова')
        decor(message, number, summa, square, choice)


def decor(message, number, summa, square, choice):
    if message.text == 'Оформить заявку':
        name_phone = bot.send_message(message.chat.id, 'Введите Имя и номер телефона')
        bot.register_next_step_handler(name_phone, order, number, summa, square, choice)
    elif message.text == 'Вернуться назад':
        cleaning(message)
    else:
        summary_buttons(message, number, summa, square, choice)


"""   ДОБАВЛЕНИЕ КНОПОК   """


def summary_buttons(message, number, summa, square, choice):
    button = types.ReplyKeyboardMarkup(True)
    button_application = types.InlineKeyboardButton('Оформить заявку')
    button_edit = types.InlineKeyboardButton('Вернуться назад')
    button.add(button_application, button_edit)
    bot.send_message(message.chat.id, 'Оформляем заявку?', reply_markup=button)
    bot.register_next_step_handler(message, decor, number, summa, square, choice)


def yes_no(message, number, choice):
    button = types.ReplyKeyboardMarkup(True)
    button_yes = types.InlineKeyboardButton('Да')
    button_no = types.InlineKeyboardButton('Нет')
    button.add(button_yes, button_no)
    bot.send_message(message.chat.id, 'Подходит такая уборка?', reply_markup=button)
    bot.register_next_step_handler(message, yes_no_click, number, choice)


def cleaning(message):
    button = types.ReplyKeyboardMarkup(True)
    one_time = types.InlineKeyboardButton('Мытьё окон, балконов')
    supportive = types.InlineKeyboardButton('Поддерживающая уборка')
    button.row(one_time, supportive)
    general = types.InlineKeyboardButton('Генеральная уборка')
    button.row(general)
    repair = types.InlineKeyboardButton('Уборка после ремонта')
    emergency = types.InlineKeyboardButton('Уборка после ЧП')
    button.row(repair, emergency)
    other = types.InlineKeyboardButton('Другое')
    edit = types.InlineKeyboardButton('Вернуться назад')
    button.row(other, edit)
    bot.send_message(message.chat.id, 'Выберите вариант уборки.', reply_markup=button)
    bot.register_next_step_handler(message, on_cleaning_click)

"""INFO IN COMPANY"""

def info_in_company(message):
    bot.send_message(message.chat.id, f'<b>Иформация о нас:</b>\n'
                f'<b>{title_url["company"][0][0]}:</b>\n{title_url["company"][0][1]}\n\n'
                f'<b>{title_url["company"][1][0]}:</b>\n{title_url["company"][1][1]}\n\n'
                f'<b>{title_url["company"][2][0]}:</b>\n{title_url["company"][2][1]}\n\n'
                f'<b>{title_url["company"][3][0]}:</b>\n{title_url["company"][3][1]}\n\n'
                f'<b>{title_url["company"][4][0]}:</b>\n{title_url["company"][4][1]}\n\n'
                f'<b>{title_url["company"][5][0]}:</b>\n{title_url["company"][5][1]}\n\n',
                parse_mode='html')

def home_page(message):
    markup = types.ReplyKeyboardMarkup(True)
    site_button = types.InlineKeyboardButton('Перейти на сайт 💻')
    order_cleaning = types.InlineKeyboardButton('Заказать уборку 🧹')
    review_button = types.InlineKeyboardButton('Оставить отзыв 📖')
    help_button = types.InlineKeyboardButton('Информация ℹ️')
    command = [order_cleaning, site_button, review_button, help_button]
    for i_command in command:
        markup.add(i_command)
    bot.send_message(message.chat.id, 'Выберите вариант действий.', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

if __name__ == '__main__':
    bot = telebot.TeleBot('6916933008:AAH8ayE-T40zuKnMKQzfVk_jeVNWr047ins')


    @bot.message_handler(commands=['start'])
    def start_main(message):
        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}. Буду рад помочь вам!')
        start_search_site()
        home_page(message)


    bot.polling(none_stop=True)
