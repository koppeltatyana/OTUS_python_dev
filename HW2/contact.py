class Contact:
    """Класс для хранения аттрибутов и методов контакта"""

    def __init__(self, name: str, phone: str, comment: str, id_: int | None = None):
        self.id_ = id_
        self.name = name
        self.phone = phone
        self.comment = comment

    def props(self) -> list[str]:
        """
        Получение списка значений аттрибутов экземпляра класса Contact

        :return: Список значений аттрибутов
        """
        return [self.__dict__[key] for key in self.__dict__]

    def to_dict(self):
        """Преобразование объекта Contact в словарь для сохранения в файл"""
        return {'id_': self.id_, 'name': self.name, 'phone': self.phone, 'comment': self.comment}

    @staticmethod
    def from_dict(data: dict):
        """Создание объекта Contact из словаря"""
        return Contact(**data)

    def __repr__(self):
        return f"{str(self.id_): >2}. {self.name: <30} {self.phone: <20} {self.comment: <25}"

    def __eq__(self, other):
        if isinstance(other, Contact):
            return self.id_ == other.id_ and\
                self.name == other.name and\
                self.phone == other.phone and\
                self.comment == other.comment
        return False
