import json
import os

from .contact import Contact


class PhoneBook:
    """Класс для хранения аттрибутов и методов телефонной книги"""

    def __init__(self, file_name: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../phone_book.json')):
        self._file_name = file_name
        self.contact_list = []
        self.saved_file = True
        self.load_contacts()

    def get_file_name(self):
        """Геттер-метод для получения защищенного аттрибута _file_name"""
        return self._file_name

    def load_contacts(self):
        """Загрузка контактов из файла"""
        file_name = self.get_file_name()
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as file:
                contacts_data = json.load(file)
                self.contact_list = [Contact.from_dict(data) for data in contacts_data]

    def save_contacts(self):
        """Сохранение контактов в файл в формате JSON"""
        with open(self.get_file_name(), 'w', encoding='utf-8') as file:
            json.dump([contact.to_dict() for contact in self.contact_list], file, ensure_ascii=False, indent=4)
        self.saved_file = True

    def generate_id(self) -> int:
        """Генерация id"""
        try:
            return max([x.id_ for x in self.contact_list]) + 1
        except ValueError:
            return 1

    def optimize_ids(self) -> None:
        """Оптимизировать id контактов"""
        for i in range(len(self.contact_list)):
            self.contact_list[i].id_ = i + 1

    def get_contact_list(self) -> list[Contact]:
        """Получение списка контактов"""
        return self.contact_list

    def add_contact(self, contact: Contact) -> None:
        """
        Добавление контакта в список контактов

        :param contact: Контакт для добавления
        """
        contact.id_ = self.generate_id() if not contact.id_ else contact.id_
        self.contact_list += [contact]
        self.saved_file = False

    def delete_contact(self, contact: Contact) -> None:
        """
        Удаление контакта из списка контактов

        :param contact: Контакт для удаления
        """
        self.contact_list.remove(contact)
        self.saved_file = False

    def edit_contact(self, old_contact: Contact, new_contact: Contact) -> None:
        """
        Редактирование контакта из списка контактов

        :param old_contact: Старые данные контакта
        :param new_contact: Новые данные контакта
        """
        for i in range(len(self.contact_list)):
            if self.contact_list[i] == old_contact:
                new_contact.id_ = old_contact.id_
                new_contact.name = old_contact.name if not new_contact.name else new_contact.name
                new_contact.phone = old_contact.phone if not new_contact.phone else new_contact.phone
                new_contact.comment = old_contact.comment if not new_contact.comment else new_contact.comment
                self.contact_list[i] = new_contact
        self.saved_file = False

    def find_contact(self, **kwargs) -> list[Contact]:
        """
        Поиск контакта из списка контактов

        :param kwargs: Именованные аргументы (нужны для поиска по переданным аттрибутам класса Contact)
        :return: Список найденных контактов
        """
        found_contacts = []

        for contact in self.contact_list:
            match = False
            for key, value in kwargs.items():
                if key == 'request_string':
                    match = bool([x for x in contact.props() if value.lower() in str(x).lower()])
                else:
                    if hasattr(contact, key) and value.lower() in getattr(contact, key).lower():
                        match = True
                        break
            if match:
                found_contacts.append(contact)
        return found_contacts

    def sort_contacts(self) -> None:
        """Сортировка контактов по полю 'Имя'"""

        self.contact_list = sorted(self.contact_list, key=lambda x: x.name)
        self.saved_file = False

    def print_contacts(self, message: str = 'Список контактов', contact_list: list[Contact] | None = None) -> None:
        """
        Печать контактов в консоль

        :param message: Сообщение перед печатью контактов
        :param contact_list: Список контактов. Если список контактов не передан, то будет распечатан полный список
        контактов
        """
        contacts = contact_list if contact_list else self.contact_list
        if not contacts:
            print('\nСписок контактов пуст\n')
        else:
            print(f'\n{message}:')
            self.print_star_str()
            for contact in contacts:
                print(contact)
            self.print_star_str(end=True)

    @staticmethod
    def print_star_str(end: bool = False):
        print('*' * 80, end='\n\n' if end else '\n')

    @staticmethod
    def print_empty_str():
        print()
