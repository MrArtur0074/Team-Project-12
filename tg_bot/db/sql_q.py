import sqlite3
from pathlib import Path

class DB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DB, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.connection = sqlite3.connect(Path(__file__).parent.parent / 'db.sqlite')
        self.cursor = self.connection.cursor()
        self._initialized = True

    def create_tables(self):
        '''Создание таблиц'''
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER
            )
        ''')
        self.connection.commit()

    def get_teachers(self):
        '''Получение всех учителей'''
        self.cursor.execute("SELECT * FROM teachers")
        return self.cursor.fetchall()

    def new_teacher(self, data: dict):
        '''Добавление нового учителя'''
        self.cursor.execute(
            "INSERT INTO teachers (tg_id) VALUES (:tg_id)",
            data
        )
        self.connection.commit()

    def get_groups(self):
        '''Получение всех групп'''
        self.cursor.execute("SELECT * FROM groups")
        return self.cursor.fetchall()

    def new_group(self, data: dict):
        '''Добавление новой группы'''
        self.cursor.execute(
            "INSERT INTO groups (group_id) VALUES (:group_id)",
            data
        )
        self.connection.commit()

    def get_admin(self):
        '''Получение администратора'''
        self.cursor.execute("SELECT * FROM admin")
        return self.cursor.fetchone()

    def set_admin(self, data: dict):
        '''Очистка таблицы и установка нового администратора'''
        self.cursor.execute("DELETE FROM admin")
        self.cursor.execute("INSERT INTO admin (admin_id) VALUES (:admin_id)", data)
        self.connection.commit()

    def clear_table(self, table_name: str):
        '''Полная очистка таблицы по имени'''
        self.cursor.execute(f"DELETE FROM {table_name}")
        self.connection.commit()
