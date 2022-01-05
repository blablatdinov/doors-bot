from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from loguru import logger

from bot_init.models import Order
from config.settings import USERS_ID

import ast 
from telebot.types import Message

users_id = ast.literal_eval(USERS_ID)
users_id = users_id


manager_buttons = ['Создать заказ', 'Информация о заказе', 'Список активных заказов']
measurer_buttons = ['Информация о заказе', 'Список активных заказов']
main_buttons = ['Да', 'Нет', 'Изменить данные', 'Принято в работу']

manager_questions = ['Введите ФИО клиента', 'Введите номер телефона', 'Введите информацию о заказе',
                    'Пожалуйста, проверьте данные:']


def user_select(id):
    """Обработчик id пользователя по словарю 'должность: id'"""
    for k, v in users_id.items():
        if v == id:
            return k


def menu_user(id):
    """Обработчик id пользователя, возвращает его должность."""
    user = user_select(id)
    return(user)


def split_name(name):
    """Обработчик ФИО клиента. Возварщает список с ФИО."""
    full_name = []
    name = name.split()
    surname_client = name[0]
    full_name.append(surname_client)
    try:
        name_client = name[1]
    except:
        name_client = '-'
    full_name.append(name_client)
    try:
        patronymic_client = name[2]
    except:
        patronymic_client = '-'
    full_name.append(patronymic_client)
    return full_name


def compile_order(part, recording_mode):
    """Обработчик данных по заказу.
    Компилируем данные во временный txt-файл до полной проверки и подтверждения."""
    with open('bot_inint/new_order.txt', recording_mode) as text_file:
        text_file.write(part)
        text_file.write('\n')


def proof_order(flag=False):
    """Обработчик данных по заказу. По умолчанию flag=False - возвращает сообщение с полной
    информацией о заказе. flag=True записывает информацию в БД."""
    with open('new_order.txt') as text_file:
        order = text_file.readlines()
        message = f'Фамилия: {order[0]}Имя: {order[1]}Отчество: {order[2]}\nТелефон: {order[3]}\nИнформация о заказе: {order[4]}'
    if flag == True:
        new_order = Order(surname_client = order[0], name_client = order[1], patronymic_client = order[2], phone_client = order[3], info = order[4])
        return message
    else:
        return message
        