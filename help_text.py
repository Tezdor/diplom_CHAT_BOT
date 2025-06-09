help_text = """
что вы хотите сделать?
        1.	/start - Начало работы с ботом.
        2.	/help - Получение справки по использованию бота.
        3.	/add_income - Добавление дохода.
        4.	/add_expense - Добавление расхода.
        5.	/history - Просмотр истории транзакций.
        6.	/goals - Управление финансовыми целями.
        7.	/report - Получение ежемесячного отчета.
        8. /nacoplenie - Добавить деньги на цель. 
        9. /sovet - Просить совета у вселенной.
        если ходите отменить действие, напишите слово "назад"
"""
def get_history_text(data, goals):
    income = []
    expense = []

    for i in data:
        if i[-2] == 'income':
            income.append(i)
        else:
            expense.append(i)

    stroka = '***ДОХОДЫ:***\n'
    for i in income:
        stroka +=f'- {i[-1]} {i[3]}\n {i[4]}\n\n' 
    
    stroka+= '\n***РАСХОДЫ:***\n'
    for i in expense:
        stroka +=f'- {i[-1]} {i[3]}\n {i[4]}\n\n' 

    stroka+= '\n***ЦЕЛИ:***\n'
    for i in goals:
        stroka +=f'- {i[2]}\n собрано {i[4]} из {i[3]}\n\n' 
    return stroka