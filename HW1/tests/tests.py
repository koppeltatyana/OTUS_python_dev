import pytest

from HW1.functions import add_item, delete_item, find_item, edit_item, FILE_DATA


class TestAdding:
    def test_add(self, generate_data: dict):
        added_item = None
        try:
            old_count = len(FILE_DATA)
            added_item = add_item(generate_data)
            assert old_count + 1 == len(FILE_DATA), f'Запись {generate_data} не была добавлена в файл'
        finally:
            delete_item(data=added_item)

class TestSearch:
    @pytest.mark.parametrize(
        'search_field, data_field_name', [('0', 'id'), ('1', 'name'), ('2', 'phone'), ('3', 'comment')]
    )
    def test_find_by_id(self, add_note, search_field, data_field_name):
        items = find_item(search_field=search_field, request_data=add_note[data_field_name])
        assert items, f'По поисковой строке {add_note["data_field_name"]} ничего не было найдено'

    @pytest.mark.parametrize(
        'search_field, data_field_name', [('*', 'id'), ('*', 'name'), ('*', 'phone'), ('*', 'comment')]
    )
    def test_find_by_string(self, add_note, search_field, data_field_name):
        items = find_item(search_field='*', request_data=add_note[data_field_name])
        assert items, f'По поисковой строке {add_note["data_field_name"]} ничего не было найдено'


class TestDelete:
    def test_delete(self, add_note_without_deleting):
        delete_item(add_note_without_deleting)
        items = find_item(request_data=add_note_without_deleting['id'], search_field='0')
        assert not items, 'Данные не были удалены'


class TestEdit:
    @pytest.mark.parametrize(
        'search_field, data_field_name', [('1', 'name'), ('2', 'phone'), ('3', 'comment')]
    )
    def test_edit_name(self, add_note, generate_data, search_field, data_field_name):
        edit_item(old_data=add_note, new_data=generate_data)
        items = find_item(search_field=search_field, request_data=generate_data[data_field_name])
        assert items, 'Записи по отредактированным данным не были получены'
