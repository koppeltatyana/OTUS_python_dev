import json
import os.path
import re
from json import JSONDecodeError


def print_star_str(end: bool = False):
    print('*' * 70, end='\n\n' if end else '\n')


FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'phone_book.json')


def write_file(data: dict, file_name: str = FILE_PATH) -> None:
    """
    Запись в файл

    :param data: Данные для записи в файл в формате словаря
    :param file_name: Наименование файла для записи
    """
    with open(file=file_name, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    global FILE_DATA
    FILE_DATA = read_file(file_name)


def read_file(file_name: str = FILE_PATH) -> list[dict]:
    """
    Чтение файла

    :param file_name: Наименование файла
    :return: Данные из файла
    """
    if not os.path.exists(file_name):
        write_file([], file_name)
    else:
        with open(file=file_name, mode='r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except JSONDecodeError:  # в случае, если файл пустой
                write_file(data=[], file_name=file_name)
                return []


FILE_DATA = read_file()


def print_items(items: list[dict] | None = None) -> None:
    """
    Вывод на консоль всех в справочнике

    :param items: Список элементов. Если элементы не переданы, то будет распечатаны все записи из справочника
    """

    global FILE_DATA
    if not FILE_DATA:
        print('Файл пустой')
    else:
        for item in items if items else FILE_DATA:
            print(f'Имя: {item["name"]}, телефон: {item["phone"]}, комментарий: {item["comment"]}')


def add_item(data: dict) -> dict:
    """
    Добавление записи в справочник

    :param data: Данные для добавления записи в формате словаря
    :return: Информация о добавленной записи (вместе с id)
    """

    global FILE_DATA
    data = {'id': generate_id(), **data}
    FILE_DATA += [data]
    write_file(FILE_DATA)  # перезаписать файл
    return data


def edit_item(old_data: dict, new_data: dict) -> None:
    """
    Редактирование записи

    :param old_data: Старые данные записи справочника
    :param new_data: Новые данные записи справочника
    """

    global FILE_DATA

    index = FILE_DATA.index(old_data)
    new_data = {'id': old_data['id'], **new_data}
    FILE_DATA[index] = new_data
    write_file(FILE_DATA)  # перезаписываем файл


def delete_item(data: dict) -> None:
    """
    Удаление записи

    :param data: Данные записи для удаления
    """

    global FILE_DATA
    try:
        FILE_DATA.remove(data)
    except ValueError:
        pass
    write_file(FILE_DATA)  # перезаписать файл


def find_item(request_data: str, search_field: str = '*') -> list[dict]:
    """
    Поиск по справочнику

    :param request_data: Поисковая строка
    :param search_field: Поле поиска
    ('0' - поиск по id, '1' - поиск по name, '2' - поиск по phone, '3' - поиск по comment)
    :return: Список найденных элементов по поисковой строке
    """

    global FILE_DATA
    if search_field == '1':
        items = list(filter(lambda x: request_data.lower() in x['name'].lower(), FILE_DATA))
    elif search_field == '2':
        items = list(filter(lambda x: request_data in x['phone'], FILE_DATA))
    elif search_field == '3':
        items = list(filter(lambda x: request_data.lower() in x['comment'].lower(), FILE_DATA))
    else:
        if search_field != '*':
            print('\nВы ввели неверный вариант, поиск данных будет произведен по всем полям')
        items = list(
            filter(
                lambda x:
                str(request_data).lower() in x['name'].lower() or
                str(request_data) in x['phone'] or
                str(request_data).lower() in x['comment'].lower(),
                FILE_DATA
            )
        )
    return items


def check_number(number: str) -> bool:
    """
    Проверить телефон на валидность

    :param number:
    :return: Булево значение
    """
    pattern = r'^[\d\s\.\-()]+$'
    return bool(re.match(pattern, number))


def generate_id() -> int:
    """
    Метод-генератор валидного идентификатора элемента справочника

    :return: Идентификатор в формате числового значения
    """
    global FILE_DATA
    return max([x['id'] for x in FILE_DATA]) + 1 if FILE_DATA else 1
