from django.core.cache import cache

from bot_init.models import Order

users_id = [['manager', 407475894], ['measurer', None]]


manager_buttons = ['Создать заказ', 'Информация о заказе', 'Список активных заказов']
measurer_buttons = ['Информация о заказе', 'Список активных заказов']
main_buttons = ['Да', 'Нет', 'Изменить данные', 'Принято в работу']

manager_questions = [
    'Введите ФИО клиента', 'Введите номер телефона', 'Введите информацию о заказе', 'Пожалуйста, проверьте данные:'
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
    """Обработчик данных по заказу. Сохраняем данные в кэш."""
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
        new_order = [full_name, phone, inform_order]
        return new_order


def writing_order_database(new_order):
    """Сохраняем данные в БД."""
    Order(name_client = new_order[0], phone_client = new_order[0], info = new_order[0])
