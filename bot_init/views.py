import telebot
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from loguru import logger

import bot_init.service as service
from bot_init.utils import get_tbot_instance

token = settings.TG_BOT.token
tbot = get_tbot_instance()
log = logger.bind(task='write_in_data')


@csrf_exempt
def bot(request):
    """Обработчик пакетов от телеграмма."""
    if request.content_type == 'application/json':
        json_data = request.body.decode('utf-8')
        log.info(json_data)
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])
        return HttpResponse('')
    else:
        raise PermissionDenied


@tbot.message_handler(commands=['start'])
def start_handler(message):
    """Обработчик команды /start."""
    user = service.menu_user(message.chat.id)
    if user is not None:
        main_menu(message)
    else:
        tbot.send_message(message.chat.id, 'hello')


@tbot.message_handler(content_types=['text'])
def main_menu(message):
    """Обработчик id пользователя."""
    user = service.menu_user(message.chat.id)
    if user == 'manager':
        manager_menu(message)
    elif user == 'measurer':
        measurer_menu(message)


def manager_menu(message):
    """Основное меню менеджера."""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in service.manager_buttons:
        markup.row(button)
    question = tbot.send_message(message.chat.id, 'Пожалуйста, выберите действие.', reply_markup=markup)
    tbot.register_next_step_handler(question, manager_action)


def measurer_menu(message):
    """Основное меню замерщика."""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in service.measurer_buttons:
        markup.row(button)
    question = tbot.send_message(message.chat.id, 'Пожалуйста, выберите действие.', reply_markup=markup)
    tbot.register_next_step_handler(question, start_handler)


def manager_action(message):
    """Обработчик команд менеджера."""
    if message.text == service.manager_buttons[0] or message.text == service.main_buttons[2]:
        question = tbot.send_message(message.chat.id, service.manager_questions[0])
        tbot.register_next_step_handler(question, create_order_1)
    else:
        measurer_menu(message)


def create_order_1(message):
    """Обработчик создания нового заказа. Фиксируем ФИО клиента. Запрашиваем телефон."""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(service.main_buttons[0], service.main_buttons[2])
    name_client = service.split_name(message.text)
    mes = f'Пожалуйста, проверьте введенные данные:\n\nФамилия: {name_client[0]}\n'
    'Имя: {name_client[1]}\nОтчество: {name_client[2]}\n\nЕсли все верно нажмите "Да"'
    question = tbot.send_message(message.chat.id, mes, reply_markup=markup)
    service.compile_order(message.chat.id, name_client, 'full_name')
    tbot.register_next_step_handler(question, create_order_2)


def create_order_2(message):
    """Уточняем правильность ФИО."""
    if message.text == service.main_buttons[0]:
        question = tbot.send_message(message.chat.id, service.manager_questions[1])
        tbot.register_next_step_handler(question, create_order_3)
    elif message.text == service.main_buttons[2]:
        manager_action(message)


def create_order_3(message):
    """Обработчик создания новогового заказа. Фиксируем телефон клиента. Запрашиваем информацию о заказе."""
    service.compile_order(message.chat.id, message.text, 'phone')
    question = tbot.send_message(message.chat.id, service.manager_questions[2])
    tbot.register_next_step_handler(question, create_order_4)


def create_order_4(message):
    """Обработчик создания новогового заказа. Фиксируем информацию о заказе. Уточняем правильность полной информации."""
    service.compile_order(message.chat.id, message.text, 'inform_order')
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(service.main_buttons[0], service.main_buttons[2])
    new_order = service.compile_order(message.chat.id, message.text)
    mes = f'Имя: {new_order[0]}\n\nТелефон клиента: {new_order[1]}\n\nИнформация о заказе: {new_order[2]}'
    mes_full = f'Пожалуйста, проверьте данные:\n\n{mes}\n\nЕсли все верно нажмите "Да"'
    question = tbot.send_message(message.chat.id, mes_full, reply_markup=markup)
    tbot.register_next_step_handler(question, save_order)


def save_order(message):
    """Обработчик создания новогового заказа. В случае правильности полной информации, записываем ее в БД."""
    if message.text == service.main_buttons[0]:
        new_order = service.compile_order(message.chat.id, message.text)
        mes = f'Имя: {new_order[0]}\n\nТелефон клиента: {new_order[1]}\n\nИнформация о заказе: {new_order[2]}'
        service.writing_order_database(new_order)
        tbot.send_message(message.chat.id, 'Заявка сохранена!')
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(service.main_buttons[3])
        tbot.send_message(service.users_id['measurer'], f'Поступила новая заявка:\n\n{mes}', reply_markup=markup)
        main_menu(message)
    elif message.text == service.main_buttons[2]:
        manager_action(message)
