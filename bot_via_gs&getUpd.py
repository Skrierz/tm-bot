import time
import telepot
import glob
from googlesheets import gs_add, summ, cards, last_4, week
from imp import reload
from pprint import pprint
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle
from telepot.namedtuple import InputTextMessageContent
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


def tm_bot():
    token = ''
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


def callback_query(msg):
    # pprint(msg)
    message_id = msg['message']['message_id']
    query_data = msg['data']
    query_router(message_id, query_data)


def query_router(message_id, query_data):
    msg_identifier = (glob.chat_id, message_id)
    types = ['yuki', 'yuki_sber', 'yuki_tink', 'yuki_stip', 'my', 'my_rocket',
             'my_sber', 'my_pskb']
    if query_data == 'add':
        tm_bot().editMessageText(msg_identifier, text='Куда добавить?',
                                 reply_markup=type_keyboard())
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
        tm_bot().sendMessage(glob.chat_id, last_4())
        reload(glob)
    elif query_data == 'week':
        week_data = week()
        d = week_data[0] + week_data[1]
        s = ('Траты за неделю: ' + str(week_data[1]) + '\nДоход за неделю: '
             + str(week_data[0]) + '\nРазница: ' + str(d))
        tm_bot().sendMessage(glob.chat_id, s)
        reload(glob)



def keyboard():
    add_butt = InlineKeyboardButton(text='Внести', callback_data='add')
    summ_butt = InlineKeyboardButton(text='Баланс', callback_data='result')
    first_row = [add_butt, summ_butt]
    buttons = [first_row]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def type_keyboard():
    yuki = InlineKeyboardButton(text='Наличные Марины',
                                callback_data='yuki')
    yuki_sber = InlineKeyboardButton(text='Сбербанк Марины',
                                     callback_data='yuki_sber')
    yuki_tink = InlineKeyboardButton(text='Тинькофф',
                                     callback_data='yuki_tink')
    yuki_stip = InlineKeyboardButton(text='Стипендиальная',
                                     callback_data='yuki_stip')
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
    fourth_row = [my_pskb, yuki_stip]
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


def digit(data):
    try:
        data = int(data)
    except ValueError as e:
        tm_bot().sendMessage(glob.chat_id, 'Необходимо числовое значение')
    else:
        glob.route = 2
        glob.collector(data)
        tm_bot().sendMessage(glob.chat_id, 'Введите комментарий:')


def comment(data):
    gs_add(*glob.collector(data))
    print(glob.collector())
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
        data = 'Сбербану Марины'
    elif data == 'yuki_tink':
        data = 'Тинькофф'
    elif data == 'yuki_stip':
        data = 'Стипендиальная'
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
    d = cards()
    mes = ('Остаток: ' + str(summ()) + '\nНаличные Марины: '
           + str(d['Наличные Марины']) + '\nСбербанк Марины: '
           + str(d['Сбербанк Марины']) + '\nТинькофф: '
           + str(d['Тинькофф']) + '\nСтипендиальная: '
           + str(d['Стипендиальная']) + '\nНаличные Андрея: '
           + str(d['Наличные Андрея']) + '\nРокетбанк: '
           + str(d['Рокетбанк']) + '\nСбербанк Андрея: '
           + str(d['Сбербанк Андрея']) + '\nПСКБ: ' + str(d['ПСКБ']))
    tm_bot().sendMessage(glob.chat_id, mes)


def main():
    MessageLoop(tm_bot(), {'inline_query': on_inline_query,
                           'chosen_inline_result': on_chosen_inline_result,
                           'chat': message,
                           'callback_query': callback_query}).run_as_thread()

    while 1:
        time.sleep(10)


if __name__ == '__main__':
    main()


