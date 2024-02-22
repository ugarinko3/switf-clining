import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import json

title_url = {}
url_site = 'https://swift-cleaning.ru/'
number = 0
summa = 0
amount_of_slaughter = [450, 65, 135, 160, 750]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                  'Safari/537.36'
}

""""  INFO IN  CLEANING  """


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


"""   SITE    """


def search(page, title):
    soup = BeautifulSoup(page, 'html.parser')

    # Service
    service = []
    info_service = []
    i = 0
    p_name_tags = soup.find_all('p', class_='textable css79')
    p_info_tags = soup.find_all('p', class_='textable css81')
    for tag_info in p_info_tags:
        info_service.append(tag_info.text)
    for tag in p_name_tags:
        list_time = [tag.text, info_service[i]]
        service.append(list_time)
        i += 1
    title['service'] = service

    # Minimal check
    info_min_price = []
    span_tags = soup.select('span', class_='textable css87')
    for i_title in span_tags:
        for a_tag in i_title:
            if 'от ' in a_tag:
                int_number = ''.join(c if c.isdigit() else ' ' for c in a_tag).split()
                num = int(int_number[0] + int_number[1])
                info_min_price.append(num)
    title['price'] = info_min_price

    # Info in cleaning
    span_info_tags = soup.find_all('p', class_='textable css152')
    info_company = []
    for i_span in span_info_tags:
        split_list = i_span.text.split(':')
        line_time = [split_list[0], split_list[1]]
        info_company.append(line_time)
    title['company'] = info_company

    return title


def site(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url=url_site))
    with open('./photo/download.gif', 'rb') as file:
        bot.send_photo(message.chat.id, file, 'Компания''\t"Swift Clining"', reply_markup=markup)
    home_page(message)


def review_site(message):
    url = 'https://yandex.ru/maps/org/svift_klining/182540269027/?ll=82.978281%2C55.044315&z=13'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url=url))
    bot.reply_to(message, 'Благодарим вас, за ваше доверие к нам!"', reply_markup=markup)
    home_page(message)


""" SUMMA CHECK """


def summ(message):
    global summa
    if message.text.isdigit():
        square = int(message.text)
        if number == 0:
            summa = square * amount_of_slaughter[0]
        elif number == 1:
            summa = square * amount_of_slaughter[1]
        elif number == 2:
            summa = square * amount_of_slaughter[2]
        elif number == 3:
            summa = square * amount_of_slaughter[3]
        elif number == 4:
            summa = square * amount_of_slaughter[4]
        if title_url['price'][number] < summa:
            bot.send_message(message.chat.id, 'Примерная сумма составила: <b>{:,}</b> рублей.'.format(summa),
                             parse_mode='html')
            summary_buttons(message)
        else:
            bot.send_message(message.chat.id, 'Извините минимальный заказ от <b>{:,}</b> рублей.\n'
                                              'Ваша сумма составила <b>{:,}</b> рублей.'
                             .format(title_url['price'][number], summa), parse_mode='html')
            yes_no_click(message)
    else:
        bot.send_message(message.chat.id, 'Произошла ошибка ввода, повторите ещё раз.')
        yes_no(message)


"""     CLICK       """


def yes_no_click(message):
    global number
    if message.text.lower() == 'да':
        if number == 0:
            sash = bot.send_message(message.chat.id, 'Сколько оконных створок?')
            bot.register_next_step_handler(sash, summ)
        else:
            square = bot.send_message(message.chat.id, 'Сколько квадратных метров?')
            bot.register_next_step_handler(square, summ)
    elif message.text.lower() == 'нет':
        cleaning(message)
    else:
        yes_no(message)


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
    else:
        bot.send_message(message.chat.id, 'Произошла ошибка ввода, повторите ещё раз')
        home_page(message)


def on_cleaning_click(message):
    global number
    command_choice = ['Разовый клининг', 'Поддерживающая уборка', 'Генеральная уборка', 'Уборка после ремонта',
                      'Уборка после ЧП', 'Другое', 'Вернуться назад']
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
    elif message.text == command_choice[6]:
        home_page(message)
    else:
        bot.send_message(message.chat.id, 'Произошла ошибка ввода, повторите ещё раз')
        cleaning(message)


def finish(message):
    if message.text == 'Оформить заявку':
        bot.send_message(message.chat.id, 'В стадии разработки')
        cleaning(message)
    elif message.text == 'Вернуться назад':
        cleaning(message)
    else:
        summary_buttons(message)


"""   ДОБАВЛЕНИЕ КНОПОК   """


def summary_buttons(message):
    button = types.ReplyKeyboardMarkup(True)
    button_application = types.InlineKeyboardButton('Оформить заявку')
    button_edit = types.InlineKeyboardButton('Вернуться назад')
    button.add(button_application, button_edit)
    bot.send_message(message.chat.id, 'Оформляем заявку?', reply_markup=button)
    bot.register_next_step_handler(message, finish)


def yes_no(message):
    button = types.ReplyKeyboardMarkup(True)
    button_yes = types.InlineKeyboardButton('Да')
    button_no = types.InlineKeyboardButton('Нет')
    button.add(button_yes, button_no)
    bot.send_message(message.chat.id, 'Подходит такая уборка?', reply_markup=button)
    bot.register_next_step_handler(message, yes_no_click)


def cleaning(message):
    button = types.ReplyKeyboardMarkup(True)
    one_time = types.InlineKeyboardButton('Разовый клининг')
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


""" INPUT IN SITE OF JSON FILE  """


def write_inf(data, file_name):
    data = json.dumps(data)
    data = json.loads(str(data))

    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


"""start search site"""


def start_search_site():
    search(requests.get(url_site).text, title_url)
    write_inf(title_url, "info_site/info_site.json")


""" function information """


def info_in_company(message):
    bot.send_message(message.chat.id, '<b>Иформация о нас:</b>\n'
                                      '<b>{}:</b>\n{}\n\n'
                                      '<b>{}:</b>\n{}\n\n'
                                      '<b>{}:</b>\n{}\n\n'
                                      '<b>{}:</b>\n{}\n\n'
                                      '<b>{}:</b>\n{}\n\n'
                     .format(title_url['company'][1][0], title_url['company'][1][1],
                             title_url['company'][2][0], title_url['company'][2][1],
                             title_url['company'][3][0], title_url['company'][3][1],
                             title_url['company'][4][0], title_url['company'][4][1],
                             title_url['company'][5][0], title_url['company'][5][1]), parse_mode='html')
    home_page(message)


if __name__ == '__main__':
    bot = telebot.TeleBot('6916933008:AAH8ayE-T40zuKnMKQzfVk_jeVNWr047ins')


    @bot.message_handler(commands=['start'])
    def start_main(message):
        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}. Буду рад помочь вам!')
        start_search_site()
        home_page(message)


    bot.polling(none_stop=True)
