import json
from datetime import datetime
from functools import reduce

if __name__ == "__main__":
    def json_decorator(file_name: str):
        """
        Декоратор для записи результатов функции в файл с переданным именем

        :param file_name: Имя файла
        """
        def inner_decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    with open(file_name, 'r', encoding='utf-8') as file:
                        file_data = json.load(file)
                except FileNotFoundError:
                    file_data = {}
                    with open(file=file_name, mode='w', encoding='utf-8') as file:
                        json.dump(file_data, file, ensure_ascii=False, indent=4)

                with open(file=file_name, mode='w', encoding='UTF-8') as file:
                    file_data[f'Имя функции: {func.__name__}. Время запуска: {datetime.now()}'] = {
                        'Результат выполнения функции': func(*args, **kwargs),
                        'Аргументы функции': {'позиционные аргументы': args, 'ключевые аргументы': kwargs},
                    }
                    json.dump(file_data, file, ensure_ascii=False, indent=4)
            return wrapper

        return inner_decorator


    @json_decorator(file_name='file_name.json')
    def custom_sum(*args):
        return reduce(lambda x, y: x + y, args)

    @json_decorator(file_name='file_name.json')
    def custom_sum_with_kwargs(**kwargs):
        return reduce(lambda x, y: x + y, kwargs.values())

    custom_sum(10, -5, -5)
    custom_sum_with_kwargs(qwe=15, asd=35)
