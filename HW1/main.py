from HW1.functions import add_item, edit_item, find_item, delete_item, print_items, print_star_str


def answers_for_search() -> (str, str):
    print(
        'Можно произвести поиск по полям:\n'
        '1. По полю "Имя"\n'
        '2. По полю "Телефон"\n'
        '3. По полю "Комментарий"\n'
        '*. Поиск сразу по всем полям\n'
    )
    find_field = input('Введите, пожалуйста, вариант из вышеперечисленных: ')
    request_str = input('Введите поисковую строку: ')
    return find_field, request_str


if __name__ == '__main__':
    while True:
        print(
            'Телефонный справочник:\n'
            '1. Показать все записи\n'
            '2. Добавить запись\n'
            '3. Найти запись\n'
            '4. Отредактировать запись\n'
            '5. Удалить запись\n'
            '0. Выход (quit/exit/0)\n\n'
        )
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
            new_data = {
                'name': input('Введите имя: '),
                'phone': input('Введите телефон: '),
                'comment': input('Введите комментарий: '),
            }
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
                        print(
                            f'Редактирование записи\n'
                            f'Имя: {item["name"]}, телефон: {item["phone"]}, комментарий: {item["comment"]}'
                        )
                        new_data = {
                            'name': input('Введите новое имя: '),
                            'phone': input('Введите новый телефон: '),
                            'comment': input('Введите новый комментарий: '),
                        }
                        edit_item(old_data=item, new_data=new_data)
                        print('Запись была успешно отредактирована')
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
    print('\nТелефонный справочник закончил работу. До встречи!\n')
