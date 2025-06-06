import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def create_pie_chart(data, title, filename):
    new_data = {}

    for i in data:
        category = i[0]
        amount = i[1]
        new_data[category] = new_data.get(category, 0) + amount
    s=sum(new_data.values())
    new_data['прочее'] = 0
    e=[]
    for k,v in new_data.items():
        if v/s<0.01 and k!='прочее':
            new_data['прочее'] += v 
            e.append(k)
    for k in e:
        del new_data[k]
    if new_data['прочее'] == 0:
        del new_data['прочее']

    labels = list(new_data.keys())
    sizes = list(new_data.values())

    fig, ax = plt.subplots(figsize=(10, 7))

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.85,
        textprops={'fontsize': 10}
    )

    ax.axis('equal')
    plt.title(title, fontsize=14, pad=20)

    try:
        plt.savefig(filename, bbox_inches='tight')
    except Exception as e:
        print("Ошибка")
# (1, 859912998, 1, 60000.0, '2025-06-02 18:19:16', 1, 'income', 'зарплата')
def create_gist_chart(data, title, filename):
    month = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сент', 'окт', 'нояб', 'дек']
    income = [0]*12
    expense = [0]*12

    for i in data:
        category = i[-2]
        amount = i[3]
        date = i[4]
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').month
        if category == 'income':
            income[date-1] +=amount
        if category == 'expense':
            expense[date-1] +=amount

    x = np.arange(len(month))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, income, width, label='income')
    rects2 = ax.bar(x + width/2, expense, width, label='expense')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(month)
    ax.legend()

    try:
        plt.savefig(filename, bbox_inches='tight')
    except Exception as e:
        print("Ошибка")

if __name__ =='__main__':
    create_pie_chart(data=[['зарплата', 10000],['лотерея', 50],['зарплата', 3000]], title='отчет', filename='1.png')

    a =  [(1, 859912998, 1, 60000.0, '2025-06-02 18:19:16', 1, 'income', 'зарплата'), (2, 859912998, 4, 6.0, '2025-06-02 18:22:01', 4, 'income', 'лотерея'), (3, 859912998, 10, 15000.0, '2025-06-02 19:03:16', 10, 'expense', 'зоотовары'), (4, 859912998, 8, 7000.0, '2025-06-02 19:03:30', 8, 'expense', 'одежда'), (5, 859912998, 11, 1000.0, '2025-06-02 19:03:39', 11, 'expense', 'транспорт'), (6, 859912998, 5, 500.0, '2025-06-02 19:04:04', 5, 'income', 'проценты по вкладу'), (7, 859912998, 1, 30000.0, '2025-06-02 19:04:13', 1, 'income', 'зарплата'), (8, 859912998, 3, 9000.0, '2025-06-02 19:04:56', 3, 'income', 'подарок'), (9, 859912998, 5, 5000.0, '2025-06-02 19:05:48', 5, 'income', 'проценты по вкладу'), (10, 859912998, 6, 6.0, '2025-06-02 19:15:12', 6, 'income', 'другое'), (11, 859912998, 2, 70.0, '2025-06-02 19:15:29', 2, 'income', 'пополнение'), (12, 859912998, 6, 312.0, '2025-06-04 17:40:14', 6, 'income', 'другое'), (13, 859912998, 3, 6000.0, '2025-06-04 19:04:27', 3, 'income', 'подарок'), (14, 859912998, 9, 500.0, '2025-06-04 19:04:37', 9, 'expense', 'кафе и рестораны')]
    create_gist_chart(data=a, title='гисторгамма', filename='2.png')