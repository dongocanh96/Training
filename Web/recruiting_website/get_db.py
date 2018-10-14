import requests
import sqlite3
conn = sqlite3.connect('website123.db')
c = conn.cursor()


def get_infos(number):
    url = 'https://api.github.com/repos/awesome-jobs/vietnam/issues/{}'
    r = requests.get(url.format(number), auth=('[my_user_name]', '[my_password]'))
    if r.status_code == 200:
        data = r.json()
        number = data['number']
        title = data['title']
        state = data['state']
        detail = data['body']
        post_date = data['created_at']
        return (number, title, state, detail, post_date)
    else:
        raise ConnectionError


def first_time_get_infos(cursor):
    for i in range(1, 1235):
        try:
            infos = get_infos(i)
        except ConnectionError:
            infos =  (i, 'blank', 'blank', 'blank', 'blank')
        finally:
            cursor.execute('''insert into jobs
                values (?, ?, ?, ?, ?)''', infos)
            conn.commit()


def update(cursor):
    last_number = cursor.execute('''select number from jobs
        order by number desc limit 1''')
    for column in last_number:
        i = column
    number = i[0] + 1
    while True:
        try:
            infos = get_infos(number)
            cursor.execute('''insert into jobs
                values (?, ?, ?, ?, ?)''', infos)
            number += 1
        except ConnectionError:
            break
    conn.commit()


def main():
    c.execute('''create table if not exists jobs
                (number integer,
                title text,
                state text,
                detail text,
                post_date text)'''
                )
    row = c.execute('select exists(select 1 from jobs limit 1)').fetchall()
    if row[0][0] == 0:
        first_time_get_infos(c)
    else:
        update(c)
    c.close()
    conn.close()


if __name__ == '__main__':
    main()
