import json
import os
from datetime import datetime
from functools import reduce


def json_decorator(file_name: str):
    """
    Декоратор для записи результатов функции в файл с переданным именем

    :param file_name: Имя файла
    """

    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            if not os.path.exists(file_name):
                file_data = {}
            else:
                with open(file_name, 'r', encoding='utf-8') as file:
                    file_data = json.load(file)

            with open(file=file_name, mode='w', encoding='UTF-8') as file:
                file_data[f'Имя функции: {func.__name__}. Время запуска: {datetime.now()}'] = {
                    'Результат выполнения функции': func(*args, **kwargs),
                    'Аргументы функции': {'позиционные аргументы': args, 'ключевые аргументы': kwargs},
                }
                json.dump(file_data, file, ensure_ascii=False, indent=4)

        return wrapper

    return inner_decorator


@json_decorator(file_name='file_name.json')
def custom_sum(*args: int):
    return reduce(lambda x, y: x + y, args)


@json_decorator(file_name='file_name.json')
def custom_sum_with_kwargs(**kwargs: dict[int]):
    return reduce(lambda x, y: x + y, kwargs.values())


if __name__ == "__main__":
    custom_sum(10, -5, -5)
    custom_sum_with_kwargs(qwe=15, asd=35)
