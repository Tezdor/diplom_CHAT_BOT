import sqlite3

class Database():
    def __init__(self,name):
        self.connection = sqlite3.connect (name)

    def add_users(self, telegram_id):
        cursor = self.connection.cursor()
        cursor.execute(""" insert or ignore into users (id,telegram_id) values(?, ?)  """, [telegram_id, telegram_id])
        self.connection.commit()

    def add_operation(self, categories, user_id, count):
        cursor = self.connection.cursor()
        cursor.execute(""" select id from categories where name = ? """, [categories])
        categories_id = cursor.fetchone()[0]
        cursor.execute(""" insert into operations (user_id, categories_id, count) values(?, ?, ?)  """, [user_id, categories_id, count])
        self.connection.commit()

    def add_goal(self, user_id, name, goal):
        cursor = self.connection.cursor()
        cursor.execute(""" insert or ignore into goals (user_id, name, goal, money) values(?, ?, ?, 0)  """, [user_id, name, goal])
        self.connection.commit()

    def add_money(self, user_id, name, money):
        cursor = self.connection.cursor()
        cursor.execute(""" select id, money, goal from goals where name = ? and user_id = ? """, [name, user_id])
        data = cursor.fetchone()

        new_money = data[1]+money
        if new_money > data[2]:
            cursor.execute(""" update goals set money = ? where id = ? """, [data[2], data[0]])
        else:
            cursor.execute(""" update goals set money = ? where id = ? """, [new_money, data[0]])
        self.connection.commit()

    def get_income_categories(self):
        cursor = self.connection.cursor()
        cursor.execute(""" select name from categories where type = 'income' """)
        data = cursor.fetchall()
        return data
    
    def get_expense_categories(self):
        cursor = self.connection.cursor()
        cursor.execute(""" select name from categories where type = 'expense' """)
        data = cursor.fetchall()
        return data
    
    def get_history(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(""" select * from operations join categories on categories.id=operations.categories_id where user_id = ? """, [user_id])
        data = cursor.fetchall()
        return data
    
    def get_goals(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(""" select * from goals where user_id = ? """, [user_id])
        data = cursor.fetchall()
        return data
    
    def get_history_30(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(""" select * from operations join categories on categories.id=operations.categories_id where user_id = ? and
                       date >= datetime('now', '-30 days') """, [user_id])
        data = cursor.fetchall()
        return data



