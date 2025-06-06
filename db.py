import sqlite3
connection = sqlite3.connect ("diplom.sqlite3")
cursor = connection.cursor()
cursor.execute(""" create table if not exists categories (
               id integer primary key autoincrement, 
               type varchar(20) not null,
               name varchar(20) not null,
               unique (type, name)
               ) """)
a = [
    ['income', 'зарплата'],
    ['income', 'пополнение'],
    ['income', 'подарок'],
    ['income', 'лотерея'],
    ['income', 'проценты по вкладу'],
    ['income', 'другое'],
    ['expense', 'супермаркет'],
    ['expense', 'одежда'],
    ['expense', 'кафе и рестораны'],
    ['expense', 'зоотовары'],
    ['expense', 'транспорт'],
    ['expense', 'другое'],
    ['expense', 'развлечения'],

]
cursor.executemany(""" insert or ignore into categories (type, name) values(?,?)  """, a)

cursor.execute(""" create table if not exists users (
               id integer primary key autoincrement,
               telegram_id integer not null unique
               ) """)

cursor.execute(""" create table if not exists operations(
               id integer primary key autoincrement,
               user_id integer not null,
               categories_id integer not null,
               count float not null,
               date datetime default current_timestamp,
               FOREIGN KEY (user_id) REFERENCES users (id),
               FOREIGN KEY (categories_id) REFERENCES categories (id)
               ) """)

cursor.execute(""" create table if not exists goals(
               id integer primary key autoincrement,
               user_id integer not null,
               name varchar(30) not null,
               goal float not null,
               money float not null,
               FOREIGN KEY (user_id) REFERENCES users (id)
               ) """)

connection.commit()

"""
создать таблицу users 
id 
telegram_id

таблица operations 
id
user_id
categories_id
count - всего

таблица goals
id
user_id
name 
goal - цель по деньгам 
money - на данный момент
"""