from random import randint

import pytest
from faker import Faker

from HW1.functions import add_item, delete_item


@pytest.fixture(scope='session')
def faker():
    return Faker('ru_RU')

@pytest.fixture
def generate_data(faker) -> dict:
    return {
        'name': faker.name(),
        'phone': faker.phone_number(),
        'comment': faker.text(max_nb_chars=randint(5, 25)),
    }


@pytest.fixture(scope='session')
def add_notes_for_test(faker):
    for _ in range(randint(5, 10)):
        add_item(
            {
                'name': faker.name(),
                'phone': faker.phone_number(),
                'comment': faker.text(max_nb_chars=randint(10, 25)),
            }
        )


@pytest.fixture
def add_note(generate_data) -> dict:
    item = add_item(generate_data)
    yield item
    delete_item(item)


@pytest.fixture
def add_note_without_deleting(generate_data) -> dict:
    item = add_item(generate_data)
    return item
