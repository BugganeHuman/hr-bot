from aiogram import Router, F, types
import secrets
import sqlite3
from aiogram.filters import Command
import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile
import os
import asyncio
from tg_bot.sheet import sheet


router = Router()

class ScreeningState(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_username = State()
    waiting_for_city = State()
    waiting_for_minimum_salary = State()
    waiting_for_skills = State()

@router.message(Command("start"))
async def start(message : types.Message):
    await message.answer('Здравствуйте! Напишите пожалуйста информацию о вас,'
                        'которую будет спрашивать бот.'
                        ' Это нужно для прохождения на следущий этап по трудоустройству.')


@router.message(ScreeningState.waiting_for_name)
async def add_candidate_name(message : types.Message, state : FSMContext):
    text = message.text