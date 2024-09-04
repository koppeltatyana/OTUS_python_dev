import json
import os.path
from random import randint

import pytest
from faker import Faker

from ..classes import Contact, PhoneBook


@pytest.fixture(scope='session')
def faker() -> Faker:
    return Faker('ru_RU')


@pytest.fixture(scope='session')
def file_for_tests():
    file_name = './phone_book_for_test.json'
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump([], file, ensure_ascii=False, indent=4)
    yield file_name
    if os.path.exists(file_name):
        os.remove(file_name)

@pytest.fixture(scope='session')
def phone_book(file_for_tests) -> PhoneBook:
    return PhoneBook(file_name=file_for_tests)

@pytest.fixture
def new_contact_data(faker: Faker, phone_book: PhoneBook) -> dict:
    return Contact(
        id_=phone_book.generate_id(),
        name=faker.name(),
        phone=faker.phone_number(),
        comment=faker.text(max_nb_chars=randint(5, 25)),
    )


@pytest.fixture(scope='session')
def add_contacts_for_test(faker: Faker, phone_book: PhoneBook):
    for _ in range(randint(5, 10)):
        phone_book.add_contact(
            Contact(name=faker.name(), phone=faker.phone_number(), comment=faker.text(max_nb_chars=randint(5, 25)))
        )
        phone_book.save_contacts()
        phone_book.load_contacts()


@pytest.fixture
def add_contact_without_deleting(new_contact_data, phone_book: PhoneBook) -> dict:
    phone_book.add_contact(new_contact_data)
    return new_contact_data


@pytest.fixture
def add_contact_with_saving_without_deleting(new_contact_data, phone_book: PhoneBook) -> dict:
    phone_book.add_contact(new_contact_data)
    phone_book.save_contacts()
    phone_book.load_contacts()
    yield new_contact_data


@pytest.fixture
def add_contact(new_contact_data, phone_book: PhoneBook) -> dict:
    phone_book.add_contact(new_contact_data)
    yield new_contact_data
    phone_book.delete_contact(new_contact_data)


@pytest.fixture
def add_contact_with_saving(new_contact_data, phone_book: PhoneBook) -> dict:
    phone_book.add_contact(new_contact_data)
    phone_book.save_contacts()
    phone_book.load_contacts()
    yield new_contact_data
    phone_book.delete_contact(new_contact_data)
    phone_book.save_contacts()
    phone_book.load_contacts()
