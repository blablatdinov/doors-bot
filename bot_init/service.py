from time import sleep

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from loguru import logger

from bot_init.utils import get_tbot_instance
from orders.models import Order

User = get_user_model()


users_test_id = [407475894, 358610865, 694285636]

my_id = users_test_id[0]

users_id = [['director', None], ['manager', None], ['measurer', my_id], ['installer', None], ['deliveryman', None]]


main_menu_button = 'Главное меню'
director_buttons = ['Информация о заказах', 'Список активных заказов', main_menu_button]
manager_buttons = ['Создать заказ', 'Информация о заказе', 'Список активных заказов', main_menu_button]
measurer_buttons = ['Информация о заказе', 'Список активных заказов', 'Поставить отметку к заказу', main_menu_button]
notice_butons = ['Принято в работу', 'Добавить примечания', main_menu_button]
main_buttons = ['Да', 'Нет', 'Изменить данные']

manager_questions = [
    'Введите ФИО клиента', 'Введите номер телефона', 'Введите информацию о заказе', 'Пожалуйста, проверьте данные:'
    ]

measurer_questions = [
    'Введите номер закза и через пробел текст', 'Пожалуйста, проверьте данные'
    ]


def user_select(id):
    """Обработчик id пользователя по словарю 'должность: id'."""
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
    except IndexError:
        name_client = '-'
    full_name.append(name_client)
    try:
        patronymic_client = name[2]
    except IndexError:
        patronymic_client = '-'
    full_name.append(patronymic_client)
    return full_name


def compile_order(id, inform, data='get_data'):
    r"""Обработчик данных по заказу. Сохраняем данные в кэш.

    TODO: рассмотреть вариант с классом

    >>> class OrderCreator:

    >>>    def set_full_name(self, manager_id, full_name):
    >>>        logger.info(f'Manager {id} set full name: {inform}')
    >>>        cache.set(f'{id}_name', f'{inform[0]}\n{inform[1]}\n{inform[2]}', 6000)

    >>>    def set_phone(self, manager_id, phone):
    >>>        logger.info(f'Manager {id} set phone: {inform}')
    >>>        cache.set(f'{id}_phone', inform, 6000)

    >>>    def get_data()
    >>>        pass
    """
    if data == 'full_name':
        logger.info(f'Manager {id} set full name: {inform}')
        cache.set(f'{id}_name', f'{inform[0]}\n{inform[1]}\n{inform[2]}', 6000)
    elif data == 'phone':
        logger.info(f'Manager {id} set phone: {inform}')
        cache.set(f'{id}_phone', inform, 6000)
    elif data == 'inform_order':
        logger.info(f'Manager {id} set order info: {inform}')
        cache.set(f'{id}_inform_order', inform, 6000)
    elif data == 'get_data':
        full_name = cache.get(f'{id}_name')
        phone = cache.get(f'{id}_phone')
        inform_order = cache.get(f'{id}_inform_order')
        new_order = [full_name, phone, inform_order]
        return new_order
    elif data == 'save_order':
        last_name, first_name, father_name = cache.get(f'{id}_name').split('\n')
        phone = cache.get(f'{id}_phone')
        inform_order = cache.get(f'{id}_inform_order')
        username = _generate_username(f'{last_name}_{first_name}')
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            father_name=father_name,
            username=username,
        )
        order = Order.objects.create(
            user=user,
            info=inform_order,
        )
        return order


def customer_registration(order_id, message_chat_id):
    """Обработка регистрации закзчика."""
    order = Order.objects.get(id=order_id)
    user = order.user
    user.chat_id = message_chat_id
    order.user_id = message_chat_id
    user.save()


def update_webhook(host=f'{settings.TG_BOT.webhook_host}/{settings.TG_BOT.token}'):
    """Обновляем webhook."""
    tbot = get_tbot_instance()
    tbot.remove_webhook()
    sleep(1)
    tbot.set_webhook(host)
    logger.info(tbot.get_webhook_info())


def _generate_username(username):
    """Генератор юзернейма."""
    logger.debug(f'Try generate username by {username}')
    counter = 1
    while True:
        if not User.objects.filter(username=username).exists():
            logger.warning(f'Username: {username} not find in database')
            return username

        username = f'{username}{counter}'
        logger.debug(f'Username: {username} find in database. Check {username}')
        counter += 1


def mark_order(user_id, order_id, text):
    """Обработчик записи отметок к заказу."""
    group = user_select(user_id)
    order = Order.objects.get(id=order_id)
    if group == 'measurer':
        order.info_from_measurer = ' '.join(text)
        order.save()
    elif group == 'installer':
        order.info_installer_datetime = ' '.join(text)
        order.save()
    elif group == 'deliveryman_datetime':
        order.deliveryman_datetime = ' '.join(text)
        order.save()
