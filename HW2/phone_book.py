import json
import os

from HW2 import Contact


class PhoneBook:
    """Класс для хранения аттрибутов и методов телефонной книги"""

    def __init__(self, file_name: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'phone_book.json')):
        self.file_name = file_name
        self.contact_list = []
        self.saved_file = True
        self.load_contacts()

    def load_contacts(self):
        """Загрузка контактов из файла"""
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                contacts_data = json.load(file)
                self.contact_list = [Contact.from_dict(data) for data in contacts_data]
        except FileNotFoundError:
            with open(file=self.file_name, mode='w', encoding='utf-8') as file:
                json.dump([], file, ensure_ascii=False, indent=4)
            self.contact_list = []  # Если файл не найден, создаем пустой список
        except json.JSONDecodeError:
            print("Ошибка при чтении файла. Файл может быть поврежден")
            self.contact_list = []

    def save_contacts(self):
        """Сохранение контактов в файл в формате JSON"""
        with open(self.file_name, 'w', encoding='utf-8') as file:
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
        print('*' * 70, end='\n\n' if end else '\n')

    @staticmethod
    def print_empty_str(end: bool = False):
        print('*' * 70, end='\n\n' if end else '\n')
