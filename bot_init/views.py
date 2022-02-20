import telebot
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from loguru import logger

from bot_init import service
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
    try:
        order_id = int(message.text.split()[1])
        service.customer_registration(order_id, message.chat.id)
        logger.info(f'{int(message.text.split()[1])}')
    except ValueError:
        pass
    if user is not None:
        main_menu(message)
    else:
        tbot.send_message(message.chat.id, 'hello')


@tbot.message_handler(content_types=['text'])
def main_menu(message):
    """Обработчик id пользователя."""
    user = service.menu_user(message.chat.id)
    if user == 'director':
        director_menu(message)
    elif user == 'manager':
        manager_menu(message)
    elif user == 'measurer':
        measurer_menu(message)
    elif user == 'installer':
        installer_menu(message)


def director_menu(message):
    """Основное меню рукводителя."""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in service.director_buttons:
        markup.row(button)
    question = tbot.send_message(message.chat.id, 'Пожалуйста, выберите действие.', reply_markup=markup)
    tbot.register_next_step_handler(question, manager_action)


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
    tbot.register_next_step_handler(question, measurer_action)


def installer_menu(message):
    """Основное меню установщика."""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in service.measurer_buttons:
        markup.row(button)
    question = tbot.send_message(message.chat.id, 'Пожалуйста, выберите действие.', reply_markup=markup)
    tbot.register_next_step_handler(question, start_handler)


def manager_action(message):
    """Обработчик команд менеджера. Запрашиваем ФИО клиента."""
    if message.text == service.manager_buttons[0] or message.text == service.main_buttons[2]:
        question = tbot.send_message(message.chat.id, service.manager_questions[0])
        tbot.register_next_step_handler(question, create_order_1)
    else:
        measurer_menu(message)


def measurer_action(message):
    """Обработчик команд замерщика."""
    if message.text == service.measurer_buttons[2]:
        question = tbot.send_message(message.chat.id, service.measurer_questions[0])
        tbot.register_next_step_handler(question, mark_to_order)
    else:
        measurer_menu(message)


def mark_to_order(message):
    """Обработчик записи отметок к заказу."""
    try:
        text = message.text.split()
        order_id = int(text[0])
        service.mark_order(message.chat.id, order_id, text[1::])
    except ValueError:
        tbot.send_message(message.chat.id, 'Что-то пошло не так...')


def create_order_1(message):
    """Обработчик создания нового заказа. Уточням ФИО клиента."""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(service.main_buttons[0], service.main_buttons[2])
    name_client = service.split_name(message.text)
    mes = (
        f'Пожалуйста, проверьте введенные данные:\n\n'
        f'Фамилия: {name_client[0]}\n'
        f'Имя: {name_client[1]}\n'
        f'Отчество: {name_client[2]}\n\n'
        'Если все верно нажмите "Да"'
    )
    question = tbot.send_message(message.chat.id, mes, reply_markup=markup)
    service.compile_order(message.chat.id, name_client, 'full_name')
    tbot.register_next_step_handler(question, create_order_2)


def create_order_2(message, flag=0):
    """Если ФИО правильно. Запрашиваем телефон."""
    if message.text == service.main_buttons[0] or flag == 1:
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
    mes = f'{new_order[0]}\n\nТелефон клиента: {new_order[1]}\n\nИнформация о заказе: {new_order[2]}'
    mes_full = f'Пожалуйста, проверьте данные:\n\n{mes}\n\nЕсли все верно нажмите "Да"'
    question = tbot.send_message(message.chat.id, mes_full, reply_markup=markup)
    tbot.register_next_step_handler(question, save_order)


def save_order(message):
    """Обработчик создания новогового заказа. В случае правильности полной информации, записываем ее в БД."""
    if message.text == service.main_buttons[0]:
        new_order = service.compile_order(message.chat.id, '', 'save_order')
        notice(new_order)
        text = (
            f'Заявка успешно сохранена.\n'
            f'Передайте заказчику ссылку: https://t.me/{settings.TG_BOT.name}?start={new_order.id}'
        )
        tbot.send_message(
            message.chat.id,
            text,
        )
    elif message.text == service.main_buttons[2]:
        create_order_2(message, flag=1)


def notice(order):
    """Отправляем данные директору и замерщику сообщение о том, что создана заявка."""
    mes = (
        f'Имя: {order.user.first_name}\n\n'
        f'Телефон клиента: {order.user.phone}\n\n'
        f'Информация о заказе: {order.info}\n\n'
        f'Номер заказа: {order.id}'
    )
    tbot.send_message(service.measurer_id, f'Поступила новая заявка:\n\n{mes}')
    tbot.send_message(service.director_id, f'Поступила новая заявка:\n\n{mes}')
