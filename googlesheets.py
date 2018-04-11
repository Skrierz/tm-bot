import gspread
import re
from time import strftime, localtime, strptime, time, sleep
from oauth2client.service_account import ServiceAccountCredentials


def gs_auth():
    scope = ['https://spreadsheets.google.com/feeds']
    secret = 'finance_secret.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(secret,
                                                                   scope)
    gs = gspread.authorize(credentials)
    return gs


def ws():
    ss = gs_auth().open_by_key('')
    ws = ss.sheet1
    return ws


def get_time():
    times = strftime("%a, %d %b %Y %H:%M:%S", localtime())
    return times


def fulltime_to_short(times):
    t = strptime(times, '%a, %d %b %Y %H:%M:%S')
    if len(str(t[1])) < 2:
        new = '0' + str(t[1])
        s = str(t[2]) + '.' + new
    else:
        s = str(t[2]) + '.' + str(t[1])
    return s


def in_week(times):
    try:
        x = strptime(times, '%a, %d %b %Y %H:%M:%S')
        t = time() - 604800
        t = localtime(t)
        if t[0] <= x[0] and t[1] <= x[1] and t[2] <= x[2]:
            return True
        else:
            return False
    except ValueError as e:
        return False


def get_row_count():
    num = ws().row_count
    return num


def gs_add(name, on_what, value, comment):
    ids = get_row_count()
    times = get_time()
    values = [ids, times, name, on_what, value, comment]
    ws().append_row(values)


def summ():
    summ = 0
    for i in ws().range(2, 5, get_row_count(), 5):
        i = str(i)
        result = re.split(r'\'', i)
        summ += int(result[1])
    return summ


def cards():
    keys = ['Наличные Марины', 'Сбербанк Марины', 'Тинькофф',
            'Наличные Андрея', 'Рокетбанк', 'Сбербанк Андрея', 'ПСКБ']
    d = dict.fromkeys(keys, 0)
    # print(d)
    for i in ws().range(2, 4, get_row_count(), 4):
        i = str(i)
        type_name = re.split(r'\'', i)[1]
        row_id = re.findall(r'\d+', i)[0]
        cell = str(ws().cell(row_id, 5))
        value = re.split(r'\'', cell)[1]
        d[type_name] = d[type_name] + int(value)
        # print(d)
        # print(value)
        sleep(0.5)
    return d


def last_4():
    string = ''
    for i in range(4):
        row = ws().row_values(get_row_count() - i)
        shrt = fulltime_to_short(row[1])
        n = '\n'
        s = f'№{row[0]}. {shrt}. {row[5]}{n}{row[3]} {row[4]}{n}{n}'
        string = string + s
    return string


def week():
    up = down = 0
    ids = get_row_count()
    data = ws().row_values(ids)
    while in_week(data[1]):
        if int(data[4]) >= 0:
            up = up + int(data[4])
        else:
            down = down + int(data[4])
        value = [up, down]
        ids = ids - 1
        data = ws().row_values(ids)
    return value

