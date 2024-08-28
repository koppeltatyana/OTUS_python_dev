from HW2 import Contact, PhoneBook


class Interface:
    """Класс для хранения аттрибутов и методов интерфейса"""

    def __init__(self, phone_book: PhoneBook):
        self.phone_book = phone_book
        self.menu_items = {
            '1': 'Печать всех контактов',
            '2': 'Добавление контакта',
            '3': 'Поиск контакта',
            '4': 'Редактирование контакта',
            '5': 'Удаление контакта',
            '6': 'Сортировка контактов',
            '7': 'Оптимизация id контактов',
            '8': 'Сохранение файла',
            '0': 'Выход'
        }
        self.search_menu = {
            '1': 'Поиск по полю "ФИО"',
            '2': 'Поиск по полю "Телефон"',
            '3': 'Поиск по полю "Комментарий"',
            '4': 'Поиск по всем полям',
        }

    @staticmethod
    def welcome_string():
        print('Телефонный справочник начал свою работу\n')

    @staticmethod
    def input_contact_data(
            name_prefix: str = 'Введите ФИО нового контакта: ',
            phone_prefix: str = 'Введите телефон нового контакта: ',
            comment_prefix: str = 'Введите комментарий для нового контакта: ',
    ):
        return Contact(name=input(name_prefix), phone=input(phone_prefix), comment=input(comment_prefix))

    def search(self) -> list[Contact]:
        """Функция-обертка для меню 'Поиск контакта'"""

        print('Можно произвести поиск по полям')
        for key, value in self.search_menu.items():
            print(f'{key: >2}. {value}')

        if (choice := input('Введите номер меню: ')) not in ['1', '2', '3', '4']:
            print('\nВы указали неверный пункт меню поиска. Повторите ввод\n')
            self.search()
        else:
            if choice == '1':
                found_contacts = self.phone_book.find_contact(
                    name=input('Введите имя, по которому необходимо искать: ')
                )
            elif choice == '2':
                found_contacts = self.phone_book.find_contact(
                    phone=input('Введите телефон, по которому необходимо искать: ')
                )
            elif choice == '3':
                found_contacts = self.phone_book.find_contact(
                    comment=input('Введите комментарий, по которому необходимо искать: ')
                )
            else:
                found_contacts = self.phone_book.find_contact(request_string=input('Введите поисковую строку: '))
            if found_contacts:
                self.phone_book.print_contacts(message='Список найденных контактов', contact_list=found_contacts)
                return found_contacts
            else:
                print('\nСреди контактов нет контакта по вашим данным')
                return []

    def editing(self) -> None:
        """Функция-обертка для меню 'Редактирование контакта'"""

        contacts_for_editing = self.search()
        if not contacts_for_editing:
            print('Для указанных данных не было найдено контактов')
            self.phone_book.print_star_str(end=True)
        else:
            if len(contacts_for_editing) > 1:
                print('\nБыло найдено больше одного контакта. Хотите отредактировать их? (y/n)')
                answer = self.yes_no_answer()
                if answer:
                    for contact in contacts_for_editing:
                        print(f'Редактируется контакт:\n{contact}')
                        self.phone_book.edit_contact(
                            old_contact=contact, new_contact=self.input_contact_data()
                        )
                    print('Контакты были отредактированы')
                    self.phone_book.print_star_str(end=True)
                else:
                    print('Выход в главное меню')
                    self.phone_book.print_star_str(end=True)
            else:
                self.phone_book.edit_contact(
                    old_contact=contacts_for_editing[0],
                    new_contact=self.input_contact_data(
                        name_prefix='Введите новое ФИО контакта: ',
                        phone_prefix='Введите новый телефон контакта: ',
                        comment_prefix='Введите новый комментарий контакта: ',
                    ),
                )
                print('Контакт был отредактирован')
                self.phone_book.print_star_str(end=True)

    def removing(self):
        """Функция-обертка для меню 'Удаление контакта'"""

        contacts_for_deleting = self.search()
        if not contacts_for_deleting:
            print('Дл указанных данных не было найдено контактов')
        else:
            if len(contacts_for_deleting) > 1:
                print('Было найдено больше одного контакта по вашим данным. Хотите удалить все? (y/n)')
                answer = self.yes_no_answer()
                if answer:
                    for contact in contacts_for_deleting:
                        self.phone_book.delete_contact(contact)
                    print('Контакты были удалены')
                else:
                    print('Выход в главное меню')
            else:
                self.phone_book.delete_contact(contacts_for_deleting[0])
                print('Контакт был удален')

    def yes_no_answer(self):
        """Функция-обертка для меню, где необходимо получить ответ 'y' или 'n'"""

        answer = input()
        if answer not in ['y', 'n']:
            print('Вы указали неверный ответ. Повторите ввод (y/n)')
            self.yes_no_answer()
        else:
            return 1 if answer == 'y' else 0

    def run_menu(self):
        """Главная функция запуска консольного меню"""

        print('-' * 12, 'МЕНЮ', '-' * 12, sep='')
        for key, value in self.menu_items.items():
            print(f'{key: >2}. {value}')

        if (choice := input('Введите номер меню: ')) != '0':
            if choice not in ['1', '2', '3', '4', '5', '6', '7']:
                print('Вы указали неверный пункт меню поиска. Повторите ввод', end='\n\n')
            else:
                # печать контактов
                if choice == '1':
                    self.phone_book.print_contacts()

                # добавление контактов
                elif choice == '2':
                    print(f'\n{self.menu_items[choice]}')
                    self.phone_book.print_star_str()
                    self.phone_book.add_contact(contact=self.input_contact_data())
                    print('Контакт был добавлен в список контактов')
                    self.phone_book.print_star_str(end=True)

                # поиск контактов
                elif choice == '3':
                    print(f'\n{self.menu_items[choice]}')
                    self.phone_book.print_star_str()
                    self.search()

                # редактирование контактов
                elif choice == '4':
                    print(f'\n{self.menu_items[choice]}')
                    self.phone_book.print_star_str()
                    print('Перед редактированием необходимо найти контакт в списке контактов')
                    self.editing()

                # удаление контактов
                elif choice == '5':
                    print(f'\n{self.menu_items[choice]}')
                    self.phone_book.print_star_str()
                    print('Перед удалением необходимо найти контакт в списке контактов')
                    self.removing()

                # сортировка контактов
                elif choice == '6':
                    print(f'\n{self.menu_items[choice]}')
                    self.phone_book.print_star_str()
                    self.phone_book.sort_contacts()
                    print('Контакты были успешно отсортированы по полю "ФИО"')
                    self.phone_book.print_star_str(end=True)

                # оптимизация id контактов
                elif choice == '7':
                    self.phone_book.print_star_str()
                    self.phone_book.optimize_ids()
                    print('Id контактов были успешно оптимизированы')
                    self.phone_book.print_star_str(end=True)

                # сохранение файла
                elif choice == '8':
                    self.phone_book.print_star_str()
                    self.phone_book.save_contacts()
                    self.phone_book.saved_file = True
                    print('Файл был успешно сохранен')
                    self.phone_book.print_star_str(end=True)

            self.run_menu()  # рекурсивный запуск метода run_menu во избежание цикла 'while True:'
        else:
            if not self.phone_book.saved_file:
                print('Данные справочника не были сохранены. Хотите сохранить их? (y/n)')
                answer = self.yes_no_answer()
                if answer:
                    self.phone_book.save_contacts()
                    print('Данные справочника сохранены')
                else:
                    print('Данные справочника не были сохранены')

            print('Телефонный справочник закончил свою работу. До свидания!')
