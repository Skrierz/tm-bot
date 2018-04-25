import time
import telepot
import telepot.api
import glob
import urllib3
from logger import Logger
from mysql import Connect
from imp import reload
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle
from telepot.namedtuple import InputTextMessageContent
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


def logs():
    format = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    logging.basicConfig(filename="main_log.log",
                        level=logging.INFO,
                        format=format)


def tm_bot():
    token = ''
    telepot.api.set_proxy('http://104.46.34.250:3128')
    bot = telepot.Bot(token)
    return bot


def on_inline_query(msg):
    reload(glob)
    query_id = msg['id']
    # pprint(msg)
    articles = [InlineQueryResultArticle(
                    id='finance',
                    title='Финансы',
                    input_message_content=InputTextMessageContent(
                        message_text='Здравствуйте'
                    )
               )]

    tm_bot().answerInlineQuery(query_id, articles)


def on_chosen_inline_result(msg):
    result_id = msg['result_id']
    # pprint(msg)
    if name_resolve(msg['from']['id']):
        if result_id == 'finance':
            tm_bot().sendMessage(glob.chat_id, 'Выберите действие',
                                 reply_markup=keyboard())
    else:
        tm_bot().sendMessage(glob.chat_id, 'У вас нет доступа к боту')


def message(msg):
    # pprint(msg)
    glob.chat_id = msg['chat']['id']
    if glob.route == 1:
        digit(msg['text'])
    elif glob.route == 2:
        comment(msg['text'])
    elif glob.route == 10:
        digit(msg['text'])
    elif glob.route == 20:
        digit(msg['text'])


def callback_query(msg):
    # pprint(msg)
    message_id = msg['message']['message_id']
    query_data = msg['data']
    query_router(message_id, query_data)


def query_router(message_id, query_data):
    msg_identifier = (glob.chat_id, message_id)
    types = ['yuki', 'yuki_sber', 'yuki_tink', 'my', 'my_rocket',
             'my_sber', 'my_pskb']
    if query_data == 'edit':
        tm_bot().editMessageText(msg_identifier, text='Что сделать?',
                                 reply_markup=edit_keyboard())
    if query_data == 'add':
        tm_bot().editMessageText(msg_identifier, text='Куда добавить?',
                                 reply_markup=type_keyboard())
    elif query_data == 'delete':
        tm_bot().editMessageText(msg_identifier,
                                 text='Введите id строки для удаления')
        glob.route = 10
    elif query_data == 'show_row':
        tm_bot().editMessageText(msg_identifier,
                                 text='Введите id строки для просмотра')
        glob.route = 20
    elif query_data == 'result':
        tm_bot().editMessageText(msg_identifier, text='Что именно интересует?',
                                 reply_markup=result_keyboard())
    elif query_data in types:
        type_resolve(query_data)
        tm_bot().sendMessage(glob.chat_id, 'Введите сумму:')
        glob.route = 1
    elif query_data == 'common':
        common()
        reload(glob)
    elif query_data == 'last_4':
        tm_bot().sendMessage(glob.chat_id, Connect().last_4())
        reload(glob)
    elif query_data == 'week':
        week_up, week_down = Connect().week()
        d = week_up + week_down
        s = ('Траты за неделю: ' + str(week_down) + '\nДоход за неделю: '
             + str(week_up) + '\nРазница: ' + str(d))
        tm_bot().sendMessage(glob.chat_id, s)
        reload(glob)


def keyboard():
    edit_butt = InlineKeyboardButton(text='Редактирование',
                                     callback_data='edit')
    summ_butt = InlineKeyboardButton(text='Баланс', callback_data='result')
    first_row = [edit_butt]
    second_row = [summ_butt]
    buttons = [first_row, second_row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def type_keyboard():
    yuki = InlineKeyboardButton(text='Наличные Марины',
                                callback_data='yuki')
    yuki_sber = InlineKeyboardButton(text='Сбербанк Марины',
                                     callback_data='yuki_sber')
    yuki_tink = InlineKeyboardButton(text='Тинькофф',
                                     callback_data='yuki_tink')
    # yuki_stip = InlineKeyboardButton(text='Стипендиальная',
    #                                  callback_data='yuki_stip')
    my = InlineKeyboardButton(text='Наличные Андрея',
                              callback_data='my')
    my_rocket = InlineKeyboardButton(text='Рокетбанк',
                                     callback_data='my_rocket')
    my_sber = InlineKeyboardButton(text='Сбербанк Андрея',
                                   callback_data='my_sber')
    my_pskb = InlineKeyboardButton(text='ПСКБ', callback_data='my_pskb')
    first_row = [my, yuki]
    second_row = [my_sber, yuki_sber]
    third_row = [my_rocket, yuki_tink]
    fourth_row = [my_pskb]
    buttons = [first_row, second_row, third_row, fourth_row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def result_keyboard():
    common = InlineKeyboardButton(text='Остаток', callback_data='common')
    last_4 = InlineKeyboardButton(text='Последние 4 действия',
                                  callback_data='last_4')
    week = InlineKeyboardButton(text='Неделя', callback_data='week')
    buttons = [[common], [last_4], [week]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def edit_keyboard():
    add_butt = InlineKeyboardButton(text='Внести', callback_data='add')
    show_row_butt = InlineKeyboardButton(text='Посмотреть строку',
                                         callback_data='show_row')
    del_butt = InlineKeyboardButton(text='Удалить строку',
                                    callback_data='delete')
    buttons = [[add_butt], [show_row_butt], [del_butt]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def digit(data):
    try:
        data = int(data)
    except ValueError as e:
        tm_bot().sendMessage(glob.chat_id, 'Необходимо числовое значение')
    else:
        if glob.route == 1:
            glob.route = 2
            glob.collector(data)
            tm_bot().sendMessage(glob.chat_id, 'Введите комментарий:')
        elif glob.route == 10:
            delete(data)
        elif glob.route == 20:
            show_row(data)


def comment(data):
    Connect().input(glob.collector(data))
    # gs_add(*glob.collector(data))
    print(glob.collector(data))
    tm_bot().sendMessage(glob.chat_id, 'Полученно')
    reload(glob)


def name_resolve(data):
    if data == 355055025:
        data = 'Андрей'
        glob.collector(data)
        return True
    elif data == 222592438:
        data = 'Марина'
        glob.collector(data)
        return True
    elif data == 333023863:
        data = 'Папа'
        glob.collector(data)
        return True
    else:
        return False


def type_resolve(data):
    if data == 'yuki':
        data = 'Наличные Марины'
    elif data == 'yuki_sber':
        data = 'Сбербанк Марины'
    elif data == 'yuki_tink':
        data = 'Тинькофф'
    # elif data == 'yuki_stip':
    #     data = 'Стипендиальная'
    elif data == 'my':
        data = 'Наличные Андрея'
    elif data == 'my_rocket':
        data = 'Рокетбанк'
    elif data == 'my_sber':
        data = 'Сбербанк Андрея'
    elif data == 'my_pskb':
        data = 'ПСКБ'
    glob.collector(data)


def common():
    summ, d = Connect().budget()
    if d['error']:
        tm_bot().sendMessage(glob.chat_id, 'Возникла ошибка в данных')
    mes = ('Остаток: ' + str(summ) + '\nНаличные Марины: '
           + str(d['Наличные Марины']) + '\nСбербанк Марины: '
           + str(d['Сбербанк Марины']) + '\nТинькофф: '
           + str(d['Тинькофф']) + '\nНаличные Андрея: '
           + str(d['Наличные Андрея']) + '\nРокетбанк: '
           + str(d['Рокетбанк']) + '\nСбербанк Андрея: '
           + str(d['Сбербанк Андрея']) + '\nПСКБ: ' + str(d['ПСКБ']))
    tm_bot().sendMessage(glob.chat_id, mes)


def delete(data):
    if Connect().lastid() >= data > 0:
        row = Connect().get_row(data)
        mes = "{0[id]} {0[date]} {0[name]} {0[type]} {0[value]} "\
              "{0[comment]}".format(row)
        Connect().delete(data)
        tm_bot().sendMessage(glob.chat_id, 'Удалена строка: {}'.format(mes))
        print('Пользователь: ', glob.values[0])
        print('Удалена строка: {}'.format(mes))
        reload(glob)
    else:
        tm_bot().sendMessage(glob.chat_id, 'Такого id не существует. '
                             'Введите валидный id.')


def show_row(data):
    if Connect().lastid() >= data > 0:
        row = Connect().get_row(data)
        mes = "{0[id]} {0[date]} {0[name]} {0[type]} {0[value]} "\
              "{0[comment]}".format(row)
        tm_bot().sendMessage(glob.chat_id,
                             'Интересующая строка: {}'.format(mes))
        print('Пользователь: ', glob.values[0])
        print('Посмотрел строку: {}'.format(mes))
        reload(glob)
    else:
        tm_bot().sendMessage(glob.chat_id, 'Такого id не существует. '
                             'Введите валидный id.')


def main():
    logs()
    try:
        MessageLoop(tm_bot(), {'inline_query': on_inline_query,
                               'chosen_inline_result': on_chosen_inline_result,
                               'chat': message,
                               'callback_query': callback_query}
                    ).run_as_thread(relax=0.5,  timeout=1)
    except urllib3.exceptions.MaxRetryError as e:
        Logger.connection_logs(e)
        telepot.api.set_proxy('http://51.254.45.80:3128')
    # else:
    #     telepot.api.set_proxy('http://104.46.34.250:3128')

    while 1:
        time.sleep(10)


if __name__ == '__main__':
    main()
