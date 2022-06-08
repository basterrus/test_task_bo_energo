import random
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import mapper, sessionmaker


class ServerStorage:
    """
    Класс - оболочка для работы с базой данных сервера.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется классический подход.
    """

    class Colors:
        """Класс таблица с цветами"""

        def __init__(self, color):
            self.id = None
            self.color = color

    def __init__(self, path):
        # Создаём движок базы данных
        self.database_engine = create_engine(f'sqlite:///{path}',
                                             echo=False,
                                             pool_recycle=7200,
                                             connect_args={'check_same_thread': False})
        # Создаём объект MetaData
        self.metadata = MetaData()

        self.blue_subject = None
        self.green_subject = None
        self.green_subject = None

        # Создаём таблицу цветов
        colors_table = Table('Colors', self.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('color', String)
                             )

        # Создаём таблицы
        self.metadata.create_all(self.database_engine)

        # Создаём отображения
        mapper(self.Colors, colors_table)

        # Создаём сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.Colors).delete()
        self.session.commit()

    # Заполняем таблицу в БД предметов цветами
    def fill_random_db(self):

        """Функция рандомно генерит последовательность цветов
        в соответствии с количеством предметов """

        max_psc_subjects = 101
        blue_subject = random.randint(60, 67)
        green_subject = blue_subject // 2
        red_subject = max_psc_subjects - blue_subject - green_subject

        list_colors = []

        for _ in range(blue_subject):
            list_colors.append('синий')
        for _ in range(green_subject):
            list_colors.append('зеленый')
        for _ in range(red_subject):
            list_colors.append('красный')
        while list_colors:
            if len(list_colors) > 1:
                index = random.randint(0, len(list_colors) - 1)
                item = list_colors.pop(index)
                random_list = self.Colors(item)
                self.session.add(random_list)
            else:
                item = list_colors.pop()
            self.session.commit()

    def find_color_by_id(self, color_id):
        color = self.session.query(self.Colors).filter_by(id=color_id).first()
        return color.color

# Отладка
# if __name__ == '__main__':
#     db = ServerStorage()
# db.fill_random_db()
# db.find_color_by_id(5)
