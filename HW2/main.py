from HW2 import PhoneBook, Interface


if __name__ == '__main__':
    phone_book = PhoneBook(file_name='phone_book.json')
    interface = Interface(phone_book=phone_book)
    interface.welcome_string()
    interface.run_menu()
