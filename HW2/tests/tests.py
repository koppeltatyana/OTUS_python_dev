from ..classes import Contact, PhoneBook


def is_contact_in_phone_book(contact: Contact, contact_list: list[Contact]) -> bool:
    """
    Проверка наличия контакта в переданном списке контактов

    :param contact: Ожидаемый контакт
    :param contact_list: Список контактов, в котором проверяем
    :return: Булево значение
    """
    return bool([x for x in contact_list if x == contact])


class TestsWithoutSaving:
    """Класс для хранения тестов без перезаписи файла"""

    def test_add_without_saving(self, new_contact_data: Contact, phone_book: PhoneBook):
        try:
            phone_book.add_contact(contact=new_contact_data)
            assert is_contact_in_phone_book(new_contact_data, phone_book.get_contact_list()),\
                f'Контакта {new_contact_data} нет в списке контактов'
        finally:
            phone_book.delete_contact(contact=new_contact_data)

    def test_find_contact_by_name(self, add_contact: Contact, phone_book: PhoneBook):
        assert phone_book.find_contact(name=add_contact.name), f'Контакт с именем "{add_contact.name}" не был найден'

    def test_find_contact_by_phone(self, add_contact: Contact, phone_book: PhoneBook):
        assert phone_book.find_contact(phone=add_contact.phone), \
            f'Контакт с телефоном "{add_contact.phone}" не был найден'

    def test_find_contact_by_comment(self, add_contact: Contact, phone_book: PhoneBook):
        assert phone_book.find_contact(comment=add_contact.comment), \
            f'Контакт с комментарием "{add_contact.comment}" не был найден'

    def test_find_contact_by_name_request_string(self, add_contact: Contact, phone_book: PhoneBook):
        assert phone_book.find_contact(request_string=add_contact.name), \
            f'Контакт по строке "{add_contact.name}" не был найден'

    def test_find_contact_by_phone_request_string(self, add_contact: Contact, phone_book: PhoneBook):
        assert phone_book.find_contact(request_string=add_contact.phone), \
            f'Контакт по строке "{add_contact.phone}" не был найден'

    def test_find_contact_by_comment_request_string(self, add_contact: Contact, phone_book: PhoneBook):
        assert phone_book.find_contact(request_string=add_contact.comment), \
            f'Контакт по строке "{add_contact.comment}" не был найден'

    def test_del(self, add_contact_without_deleting: Contact, phone_book: PhoneBook):
        phone_book.delete_contact(contact=add_contact_without_deleting)
        assert not is_contact_in_phone_book(add_contact_without_deleting, phone_book.get_contact_list()),\
            f'Контакт {add_contact_without_deleting} есть в списке даже после удаления'

    def test_edit(self, add_contact: Contact, new_contact_data: Contact, phone_book: PhoneBook):
        phone_book.edit_contact(old_contact=add_contact, new_contact=new_contact_data)
        assert is_contact_in_phone_book(new_contact_data, phone_book.get_contact_list()), \
            f'Данные контакта {add_contact} не были отредактированы'

    def test_id_optimize(self, add_contacts_for_test, add_contact_without_deleting, phone_book: PhoneBook):
        phone_book.delete_contact(add_contact_without_deleting)
        phone_book.optimize_ids()
        contact_ids_list = [x.id_ for x in phone_book.get_contact_list()]
        assert min(contact_ids_list) == 1 and max(contact_ids_list) == len(contact_ids_list),\
            'Id контактов не были оптимизированы'

    def test_sort(self, phone_book: PhoneBook):
        phone_book.sort_contacts()
        assert sorted(
            [x.name for x in phone_book.get_contact_list()]
        ) == [x.name for x in phone_book.get_contact_list()], 'Сортировка не была произведена'


class TestsWithSaving:
    """Класс для хранения тестов c перезаписью файла"""

    def test_add_saving(self, new_contact_data: Contact, phone_book: PhoneBook):
        try:
            phone_book.add_contact(contact=new_contact_data)
            phone_book.save_contacts()
            phone_book.load_contacts()
            assert is_contact_in_phone_book(new_contact_data, phone_book.get_contact_list()),\
                f'Контакта {new_contact_data} нет в списке контактов'
        finally:
            phone_book.delete_contact(contact=new_contact_data)
            phone_book.save_contacts()
            phone_book.load_contacts()

    def test_del_saving(self, add_contact_with_saving_without_deleting: Contact, phone_book: PhoneBook):
        phone_book.delete_contact(contact=add_contact_with_saving_without_deleting)
        phone_book.save_contacts()
        phone_book.load_contacts()
        assert not is_contact_in_phone_book(
            add_contact_with_saving_without_deleting, phone_book.get_contact_list()
        ), 'Контакт есть в списке даже после удаления'

    def test_edit_saving(self, add_contact_with_saving: Contact, new_contact_data: Contact, phone_book: PhoneBook):
        try:
            phone_book.edit_contact(old_contact=add_contact_with_saving, new_contact=new_contact_data)
            phone_book.save_contacts()
            phone_book.load_contacts()
            assert is_contact_in_phone_book(new_contact_data, phone_book.get_contact_list()), \
                f'Данные контакта {add_contact_with_saving} не были отредактированы'
        finally:
            phone_book.edit_contact(old_contact=new_contact_data, new_contact=add_contact_with_saving)
            phone_book.save_contacts()
            phone_book.load_contacts()

    def test_id_optimize_saving(self, add_contacts_for_test, add_contact_with_saving_without_deleting, phone_book):
        phone_book.delete_contact(add_contact_with_saving_without_deleting)
        phone_book.optimize_ids()
        phone_book.save_contacts()
        phone_book.load_contacts()
        contact_ids_list = [x.id_ for x in phone_book.get_contact_list()]
        assert min(contact_ids_list) == 1 and max(contact_ids_list) == len(contact_ids_list),\
            'Id контактов не были оптимизированы'

    def test_sort_saving(self, phone_book: PhoneBook):
        try:
            phone_book.sort_contacts()
            phone_book.save_contacts()
            phone_book.load_contacts()
            assert sorted(
                [x.name for x in phone_book.get_contact_list()]
            ) == [x.name for x in phone_book.get_contact_list()], 'Сортировка не была произведена'
        finally:
            phone_book.optimize_ids()
            phone_book.save_contacts()
            phone_book.load_contacts()
