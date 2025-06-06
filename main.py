from utils import Database
import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, html, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from images import create_pie_chart, create_gist_chart
from help_text import help_text
from dotenv import load_dotenv
load_dotenv()

def escape_markdown(text: str) -> str:
    escape_chars = '[]()~>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

st = MemoryStorage()
class Income(StatesGroup):
    categories = State()
    money = State()

class Expense(StatesGroup):
    categories = State()
    money = State()

class Goal(StatesGroup):
    name = State()
    goal_in_money = State()

class Money(StatesGroup):
    name = State()
    money = State() 

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv('TOKEN')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# All handlers should be attached to the Router (or Dispatcher)

dp = Router()
db = Database('diplom.sqlite3')


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    db.add_users(message.from_user.id)
    await message.answer(f"здравствуйте, {html.bold(message.from_user.full_name)}!")



@dp.message(Command('help'))
async def command_help_handler(message: Message):
    await message.answer(help_text)

# @dp.message(Command('categories'))
# async def command_categories_handler(message: Message):
#     keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[KeyboardButton(text = 'доход'), KeyboardButton(text = 'расход')]])
#     await message.answer("какую категорию вы хотите добавить?", reply_markup=keyboard)

@dp.message(Command('add_income'))
async def command_add_income_hendler(message: Message, state: FSMContext):
    await state.set_state(Income.categories)
    data = db.get_income_categories()
    buttons = [[KeyboardButton(text=text[0])] for text in data] + [[KeyboardButton(text='назад')]]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=buttons)
    await message.answer("какой доход вы хотите добавить?", reply_markup=keyboard)

@dp.message( Income.categories)
async def command_income_money_hendler(message: Message, state: FSMContext):
    if message.text == 'назад':
        await state.clear()
        await message.answer('отменено')
        return
    
    data = db.get_income_categories()
    if (message.text, ) not in data:
        buttons = [[KeyboardButton(text=text[0])] for text in data] + [[KeyboardButton(text='назад')]]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=buttons)
        await message.answer('такой категории нет, выберите из списка', reply_markup=keyboard)
    else:
        await state.update_data(categories = message.text)
        await state.set_state(Income.money)
        await message.answer('Сколько денег вы получили?')

@dp.message( Income.money)
async def command_income_hendler( message: Message, state: FSMContext):
    if message.text == 'назад':
        await state.clear()
        await message.answer('отменено')
        return
    
    money = message.text.replace(',', '.') 
    try:
        float(money)
        categories = await state.get_data()
        categories = categories['categories']
        db.add_operation(categories=categories, user_id=message.from_user.id, count=money)
        await state.clear()
        await message.answer('gotovo')
    except ValueError:
        await message.answer('введите число')
    

@dp.message(Command('add_expense'))
async def command_add_expense_hendler(message: Message, state:FSMContext):
    await state.set_state(Expense.categories)
    data = db.get_expense_categories()
    buttons = [[KeyboardButton(text=text[0])] for text in data] + [[KeyboardButton(text='назад')]]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=buttons)
    await message.answer("какой расход вы хотите добавить?", reply_markup=keyboard)

@dp.message( Expense.categories)
async def command_income_money_hendler(message: Message, state: FSMContext):
    if message.text == 'назад':
        await state.clear()
        await message.answer('отменено')
        return
    
    data = db.get_expense_categories()
    if (message.text, ) not in data:
        buttons = [[KeyboardButton(text=text[0])] for text in data] + [[KeyboardButton(text='назад')]]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=buttons)
        await message.answer('такой категории нет, выберите из списка', reply_markup=keyboard)
    else:
        await state.update_data(categories = message.text)
        await state.set_state(Expense.money)
        await message.answer('Сколько денег вы потратили?')

@dp.message( Expense.money)
async def command_expense_hendler( message: Message, state: FSMContext):
    if message.text == 'назад':
        await state.clear()
        await message.answer('отменено')
        return
    
    money = message.text.replace(',', '.') 
    try:
        float(money)
        categories = await state.get_data()
        categories = categories['categories']
        db.add_operation(categories=categories, user_id=message.from_user.id, count=money)
        await state.clear()
        await message.answer('done')  
    except ValueError:
        await message.answer('введите число')
       


@dp.message(Command('goals'))
async def command_add_goal_hendler(message: Message, state:FSMContext):
    await state.set_state(Goal.name)
    await message.answer("на что копите?")

@dp.message( Goal.name)
async def command_goal_goal_hendler(message: Message, state: FSMContext):
    if message.text == 'назад':
        await state.clear()
        await message.answer('отменено')
        return
    
    await state.update_data(name = message.text)
    await state.set_state(Goal.goal_in_money)
    await message.answer('Сколько денег вы хотели бы накопить?')

@dp.message( Goal.goal_in_money)
async def command_goal_hendler( message: Message, state: FSMContext):
    if message.text == 'назад':
        await state.clear()
        await message.answer('отменено')
        return
    
    goal = message.text.replace(',', '.') 
    try:
        float(goal)
        name = await state.get_data()
        name = name['name']
        db.add_goal(name=name, user_id=message.from_user.id, goal=goal)
        await state.clear()
        await message.answer('yes') 
    except ValueError:
        await message.answer('введите число')

@dp.message(Command('nacoplenie'))
async def command_nacoplenie_hendler(message: Message, state:FSMContext):
    await state.set_state(Money.name)
    data = db.get_goals(message.from_user.id)
    buttons = [[KeyboardButton(text=text[2])] for text in data] + [[KeyboardButton(text='назад')]]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=buttons)
    await message.answer("на какую цель добавить деньги?", reply_markup = keyboard)

@dp.message(Money.name)
async def command_nacoplenie_money_hendler(message: Message, state: FSMContext):
    if message.text == 'назад':
        await state.clear()
        await message.answer('отменено')
        return
    
    data = db.get_goals(message.from_user.id)
    g = [i[2] for i in data]
    if message.text not in g:
        buttons = [[KeyboardButton(text=text[2])] for text in data] + [[KeyboardButton(text='назад')]]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=buttons)
        await message.answer('такой цели нет, выберите из списка', reply_markup=keyboard)
    else:
        await state.update_data(name = message.text)
        await state.set_state(Money.money)
        await message.answer('Сколько денег вы хотели бы добавить?')

@dp.message( Money.money)
async def command_nacoplenie_goals_hendler( message: Message, state: FSMContext):
    if message.text == 'назад':
        await state.clear()
        await message.answer('отменено')
        return
    
    money = message.text.replace(',', '.') 
    try:
        float(money)
        name = await state.get_data()
        name = name['name']
        db.add_money(name=name, user_id=message.from_user.id, money=float(money))
        await state.clear()
        await message.answer('yes')
        
    except ValueError:
        await message.answer('введите число')
    

@dp.message(Command('history'))
async def history_hendler(message: Message):
    data = db.get_history_30(user_id=message.from_user.id)
    goals = db.get_goals(user_id=message.from_user.id)

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
    
    """ 
    доходы: 
    зарплата 6890
    кот 1568390
    итого: 567890

    расходы:
    кот 4699
    это 56698
    итого: 456789

    цели накопления:
    цель собака
    накоплено 456789 из 456789

    цель дом

    """
    await message.answer(escape_markdown(stroka), parse_mode='MarkdownV2')

@dp.message(Command('report'))
async def report_hendler(message:Message):

    data = db.get_history(user_id=message.from_user.id)
    data2 = db.get_history_30(user_id=message.from_user.id)

    income = []
    expense = []

    for i in data2:
        if i[-2] == 'income':
            income.append([i[-1], i[3]])
        else:
            expense.append([i[-1], i[3]])
    f1 = f'{message.from_user.id}_income.png'
    f2 = f'{message.from_user.id}_expense.png'
    f3 = f'{message.from_user.id}_all.png'
    create_pie_chart(data=income, title='ежемесячный отчет о доходах', filename=f1)
    create_pie_chart(data=expense, title='ежемесячный отчет о расходах', filename=f2)
    create_gist_chart(data=data, title='транзакции за весь год', filename=f3)
    png1 = FSInputFile(f1)
    png2 = FSInputFile(f2)
    png3 = FSInputFile(f3)
    await bot.send_photo(chat_id=message.chat.id, photo=png1)
    await bot.send_photo(chat_id=message.chat.id, photo=png2)
    await bot.send_photo(chat_id=message.chat.id, photo=png3)

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.answer(help_text)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls

    dis = Dispatcher(storage=st)
    dis.include_router(dp)
    # And the run events dispatching
    await dis.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

    # goals and expenses