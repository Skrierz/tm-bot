import MySQLdb
from time import strftime, localtime, strptime, time
from configparser import ConfigParser


class Connect:

    def open(self):
        self.op = MySQLdb.connect(**config())
        self.cur = self.op.cursor(MySQLdb.cursors.DictCursor)

    def close(self):
        self.cur.close()
        self.op.close()

    def input(self, atr):
        self.open()
        times = get_time()
        atr.append(times)
        txt = "INSERT INTO budget_changes (date, name, type, value, comment)"\
              "VALUES"\
              "('{0[4]}', '{0[0]}', '{0[1]}', '{0[2]}', '{0[3]}')".format(atr)
        self.cur.execute(txt)
        self.op.commit()
        self.close()

    def budget(self):
        summ = 0
        keys = ['Наличные Марины', 'Сбербанк Марины', 'Тинькофф',
                'Наличные Андрея', 'Рокетбанк', 'Сбербанк Андрея', 'ПСКБ']
        d = dict.fromkeys(keys, 0)
        self.open()
        self.cur.execute('SELECT type, value FROM budget_changes')
        data = self.cur.fetchall()
        for string in data:
            summ += string['value']
            try:
                d[string['type']] += string['value']
            except KeyError as e:
                d['error'] = [e]
                print(d['error'])
        self.close()
        return summ, d

    def last_4(self):
        string = ''
        n = '\n'
        self.open()
        lastid = self.cur.execute('SELECT * FROM budget_changes')
        query = 'SELECT * FROM budget_changes WHERE id > {}'.format(lastid - 4)
        self.cur.execute(query)
        data = self.cur.fetchall()
        for i in range(len(data)):
            shrt = fulltime_to_short(data[i]['date'])
            s = f"№{data[i]['id']}. {shrt}. {data[i]['comment']}{n}"\
                f"{data[i]['type']} {data[i]['value']}{n}{n}"
            string += s
        return string

    def week(self):
        up = down = 0
        self.open()
        self.cur.execute('SELECT * FROM budget_changes ORDER BY id DESC')
        data = self.cur.fetchone()
        while in_week(data['date']):
            if data['value'] >= 0:
                up += data['value']
            else:
                down += data['value']
            data = self.cur.fetchone()
        self.close()
        return up, down

    def lastid(self):
        self.open()
        lastid = self.cur.execute("SELECT * FROM budget_changes")
        self.close()
        return lastid

    def get_row(self, idx):
        self.open()
        txt = "SELECT * FROM budget_changes WHERE id = {}".format(idx)
        self.cur.execute(txt)
        row = self.cur.fetchone()
        self.close()
        return row

    def delete(self, idx):
        lastid = Connect().lastid()
        self.open()
        txt = ('INSERT INTO deleted SELECT * FROM budget_changes WHERE id = {}'
               .format(idx))
        self.cur.execute(txt)
        self.op.commit()
        txt = "DELETE FROM budget_changes WHERE id = {}".format(idx)
        self.cur.execute(txt)
        self.op.commit()
        for i in range(idx, lastid):
            txt = "UPDATE budget_changes SET id = {} WHERE "\
                  "budget_changes.id = {}".format(i, i+1)
            self.cur.execute(txt)
            self.op.commit()
        self.cur.execute("ALTER TABLE budget_changes AUTO_INCREMENT "
                         "= {}".format(lastid-1))
        self.op.commit()
        self.close()


def config(filename='config.ini', section='budget_changes'):
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            config[item[0]] = item[1]
    else:
        raise Exception('{0} not found in {1} file'.format(section, filename))
    return config


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
