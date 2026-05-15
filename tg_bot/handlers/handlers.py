from aiogram import Router, F, types
from aiogram.filters import Command
import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import os
import asyncio
from tg_bot.sheet import sheet
from tg_bot.keyboards import get_end_screening_panel


router = Router()

class ScreeningState(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_username = State()
    waiting_for_city = State()
    waiting_for_minimum_salary = State()
    waiting_for_skills = State()

@router.message(Command("start"))
async def start(message : types.Message, state : FSMContext):
    await message.answer('Здравствуйте! Напишите пожалуйста информацию о вас,'
                        'которую будет спрашивать бот.'
                        ' Это нужно для прохождения на следущий этап по трудоустройству.')
    await message.answer('Напиши свое имя')
    await state.set_state(ScreeningState.waiting_for_name)


@router.message(ScreeningState.waiting_for_name)
async def add_candidate_name(message : types.Message, state : FSMContext):
    name = message.text
    if len(name) > 200:
        await message.answer('Напиши свое имя, максимальная длинна 200 символов')
        await state.set_state(ScreeningState.waiting_for_name)
        return
    await state.update_data(candidate_name=name)
    await message.answer('Напиши свой возраст')
    await state.set_state(ScreeningState.waiting_for_age)

@router.message(ScreeningState.waiting_for_age)
async def add_candidate_age(message : types.Message, state : FSMContext):
    age = message.text
    try:
        if int(age) > 150 or int(age) < 16:
            raise ValueError
    except Exception as e:
        await message.answer('Напиши свой возраст, например 20')
        await state.set_state(ScreeningState.waiting_for_age)
        return
    await state.update_data(candidate_age=age)
    await message.answer('Напиши свой юзернейм в телеграмм, через собачку (@)')
    await state.set_state(ScreeningState.waiting_for_username)

@router.message(ScreeningState.waiting_for_username)
async def add_candidate_username(message : types.Message, state : FSMContext):
    username = message.text
    if not username.startswith('@'):
        await message.answer('Напиши свой юзернейм в телеграмм, через @, например @example')
        await state.set_state(ScreeningState.waiting_for_username)
        return
    await state.update_data(candidate_username=username)
    await message.answer('Напиши свой город')
    await state.set_state(ScreeningState.waiting_for_city)

@router.message(ScreeningState.waiting_for_city)
async def add_candidate_city(message : types.Message, state : FSMContext):
    city = message.text
    await state.update_data(candidate_city=city)
    await message.answer('Напиши свои минимальные ожидания от зарплаты')
    await state.set_state(ScreeningState.waiting_for_minimum_salary)

@router.message(ScreeningState.waiting_for_minimum_salary)
async def add_candidate_minimum_salary(message : types.Message, state : FSMContext):
    minimum_salary = message.text
    try:
        if int(minimum_salary) < 0:
            raise ValueError
    except Exception as e:
        await message.answer('Напиши свои минимальные ожидания от зарплаты цифрой, например 35000')
        await state.set_state(ScreeningState.waiting_for_minimum_salary)
        return
    await state.update_data(candidate_minimum_salary=minimum_salary)
    await message.answer('Напиши свои навыки')
    await state.set_state(ScreeningState.waiting_for_skills)

@router.message(ScreeningState.waiting_for_skills)
async def add_candidate_skills(message : types.Message, state : FSMContext):
    skills = message.text
    if len(skills) < 3:
        await message.answer('Напиши свои навыки, если думаешь что у тебя их нет'
                                ' напиши просто что ты умеешь делать хорошо')
        await state.set_state(ScreeningState.waiting_for_skills)
        return
    await state.update_data(candidate_skills=skills)
    await message.answer('Заполнение анкеты завершенно', reply_markup=get_end_screening_panel())

@router.callback_query(F.data == 'end_screening')
async def send_candidate_data_to_sheet(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    data = await state.get_data()
    name = data['candidate_name']
    age = data['candidate_age']
    username = data['candidate_username']
    city = data['candidate_city']
    minimum_salary = data['candidate_minimum_salary']
    skills = data['candidate_skills']
    status = 'screening'
    try:
        sheet.append_row([name, age, username, city, minimum_salary, skills, status])
    except Exception as e:
        print(e)
    await state.clear()
    await callback.message.edit_text('Спасибо, анкета принята')