import re
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from loguru import logger
from django.core.cache import cache

from bot_init.models import Order

import ast 



users_id = [['manager', 407475894], ['measurer', None]]


manager_buttons = ['Создать заказ', 'Информация о заказе', 'Список активных заказов']
measurer_buttons = ['Информация о заказе', 'Список активных заказов']
main_buttons = ['Да', 'Нет', 'Изменить данные', 'Принято в работу']

manager_questions = ['Введите ФИО клиента', 'Введите номер телефона', 'Введите информацию о заказе',
                    'Пожалуйста, проверьте данные:']


def user_select(id):
    """Обработчик id пользователя по словарю 'должность: id'"""
    for i in users_id:
        if i[1] == id:
            return i[0]


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



def compile_order(id, inform, data='get_data'):
    """Обработчик данных по заказу. Сохраняем ФИО в кэш."""
    if data == 'full_name':
        cache.set(f'{id}_name', f'Фамиля: {inform[0]}\nИмя: {inform[1]}\nОтчество: {inform[2]}', 6000)
    elif data == 'phone':
        cache.set(f'{id}_phone', inform, 6000)
    elif data == 'inform_order':
        cache.set(f'{id}_inform_order', inform, 6000)
    elif data == 'get_data':
        full_name = cache.get(f'{id}_name')
        phone = cache.get(f'{id}_phone')
        inform_order = cache.get(f'{id}_inform_order')
        mes = f'{full_name}\n\nТелефон клиента: {phone}\n\nИнформация о заказе: {inform_order}'
        return mes





# def compile_order(part, recording_mode):
#     """Обработчик данных по заказу.
#     Компилируем данные во временный txt-файл до полной проверки и подтверждения."""
#     with open('new_order.txt', recording_mode) as text_file:
#         text_file.write(part)
#         text_file.write('\n')


# def proof_order(flag=False):
#     """Обработчик данных по заказу. По умолчанию flag=False - возвращает сообщение с полной
#     информацией о заказе. flag=True записывает информацию в БД."""
#     with open('new_order.txt') as text_file:
#         order = text_file.readlines()
#         message = f'Фамилия: {order[0]}Имя: {order[1]}Отчество: {order[2]}\nТелефон: {order[3]}\nИнформация о заказе: {order[4]}'
#     if flag == True:
#         new_order = Order(surname_client = order[0], name_client = order[1], patronymic_client = order[2], phone_client = order[3], info = order[4])
#         return message
#     else:
#         return message
        