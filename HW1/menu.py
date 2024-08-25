from functions import add_item, check_number, edit_item, find_item, delete_item, print_items, print_star_str


def answers_for_search() -> (str, str):
    search_menu = [
        '\t1. По полю "Имя"',
        '\t2. По полю "Телефон"',
        '\t3. По полю "Комментарий"',
        '\t*. Поиск сразу по всем полям',
    ]
    print('Можно произвести поиск по полям\n', '\n'.join(search_menu), end='\n')
    find_field = input('Введите, пожалуйста, вариант из вышеперечисленных: ')
    request_str = input('Введите поисковую строку: ')
    return find_field, request_str


def start_menu():
    while True:
        menu_items = [
            '\t1. Показать все записи',
            '\t2. Добавить запись',
            '\t3. Найти запись',
            '\t4. Отредактировать запись',
            '\t5. Удалить запись',
            '\t0. Выход (quit/exit/0)'
        ]
        print('Телефонный справочник\n', '\n'.join(menu_items), end='\n')
        answer = input('Введите номер меню: ')
        if answer in ['0', 'exit', 'quit', 'q', 'e']:
            break

        elif answer == '1':
            print_star_str()
            print('Данные в справочнике:')
            print_items()
            print_star_str(end=True)

        elif answer == '2':
            print_star_str()
            new_data = {'name': input('Введите имя: ')}
            phone = input('Введите телефон: ')
            while True:
                if check_number(phone):
                    new_data.update(phone=phone, comment=input('Введите комментарий: '))
                    break
                phone = input('Неверный формат телефона. Разрешаются символы: 0-9, -, ., ()\nВведите телефон еще раз: ')

            add_item(new_data)
            print(
                f'Были добавлены данные в справочник:\n'
                f'Имя: {new_data["name"]}, телефон: {new_data["phone"]}, комментарий: {new_data["comment"]}'
            )
            print_star_str(True)

        elif answer == '3':
            print_star_str()
            find_answer, request_data = answers_for_search()
            found_items = find_item(request_data=request_data, search_field=find_answer)
            if not found_items:
                print(f'Данных по вашему запросу "{request_data}" не найдено')
            else:
                print('По вашему запросу были найдены записи:')
                print_items(found_items)
            print_star_str(True)

        elif answer == '4':
            print_star_str()
            print('Для начала найдем записи для редактирования')
            find_answer, request_data = answers_for_search()
            items_for_editing = find_item(request_data=request_data, search_field=find_answer)

            if not items_for_editing:
                print(f'Данных по вашему запросу "{request_data}" не найдено')
            else:
                print('Будут отредактированы записи:')
                print_items(items_for_editing)
                answer = input('Продолжить? (y/n)\n')
                if answer in ['y', '']:
                    for item in items_for_editing:
                        print_star_str()
                        print(
                            f'Редактирование записи\n'
                            f'Имя: {item["name"]}, телефон: {item["phone"]}, комментарий: {item["comment"]}'
                        )
                        new_data = {'name': input('Введите имя: ')}
                        phone = input('Введите телефон: ')
                        while True:
                            if check_number(phone):
                                new_data.update(phone=phone, comment=input('Введите комментарий: '))
                                break
                            phone = input(
                                'Неверный формат телефона. Разрешаются символы: 0-9, -, ., ()\n'
                                'Введите телефон еще раз: '
                            )
                        edit_item(old_data=item, new_data=new_data)
                        print('Запись была успешно отредактирована')
                        print_star_str()
                else:
                    print('Записи не были отредактированы')
            print_star_str(True)

        elif answer == '5':
            print_star_str()
            print('Для начала найдем записи для удаления')
            find_answer, request_data = answers_for_search()
            items_for_del = find_item(request_data=request_data, search_field=find_answer)

            if not items_for_del:
                print(f'Данных по вашему запросу "{request_data}" не найдено')
            else:
                print('Будут удалены записи:')
                print_items(items_for_del)
                answer = input('Продолжить? (y/n)\n')
                if answer in ['y', '']:
                    for item in items_for_del:
                        delete_item(data=item)
                    print('Записи были успешно удалены из справочника')
                else:
                    print('Записи не были удалены')
            print_star_str(True)

        else:
            incorrect_answer = input('Вы указали неверный пункт меню. Хотите продолжить (y/n)?\n')
            if incorrect_answer == 'n':
                break