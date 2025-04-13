import sqlite3
from pathlib import Path


def init_db():
    """
    Создается соединение с БД и курсор
    """
    global db, cursor
    db = sqlite3.connect(
        Path(__file__).parent.parent / "db.sqlite"
    )
    cursor = db.cursor()

def create_tables():
    """
    Создание таблиц
    """
    cursor.execute("""
        --sql
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER
        );
    """)

    cursor.execute("""
        --sql
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER
        );
    """)

    cursor.execute("""
        --sql
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER
        );
    """)

    db.commit()


def get_teachers():
    """
    Получение данных о всех курсах
    """
    cursor.execute("""
        SELECT tg_id FROM teachers
    """)
    return cursor.fetchall()



def new_teacher(data: dict):
    cursor.execute("""
        --sql
        INSERT INTO teachers (tg_id) VALUES
        (:user_id)
    """, data)
    db.commit()


def get_group():
    """
    Получение данных о всех курсах
    """
    cursor.execute("""
        SELECT * FROM groups
    """)
    return cursor.fetchall()



def new_group(data: dict):
    cursor.execute("""
        --sql
        INSERT INTO groups (group_id) VALUES
        (:group_id)
    """, data)
    db.commit()


def get_admin():
    """
    Получение данных о всех курсах
    """
    cursor.execute("""
        SELECT admin_id FROM admin
    """)
    return cursor.fetchall()


def set_admin(data: dict):
    # Очистка таблицы
    cursor.execute("DELETE FROM admin")

    # Вставка нового администратора
    cursor.execute("""
        INSERT INTO admin (admin_id) VALUES
        (:user_id)
    """, data)

    db.commit()


if __name__ == "__main__":
    init_db()
    create_tables()
    teachers = [i[0] for i in get_teachers()]
    print(teachers)