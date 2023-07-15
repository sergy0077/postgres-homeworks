import json
import psycopg2
from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'

    params = config()
    conn = None

    # Проверяем наличие базы данных и решаем, что делать
    if database_exists(params, db_name):
        response = input(f"БД {db_name} уже существует. Удалить и создать заново? (y/n): ")
        if response.lower() == 'y':
            drop_database(params, db_name)
            print(f"БД {db_name} удалена")
        else:
            print(f"Используем существующую БД {db_name}")
    else:
        create_database(params, db_name)
        print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def database_exists(params, db_name):
    """Проверяет наличие базы данных с заданным именем."""
    try:
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT datname FROM pg_database WHERE datname = '{db_name}'")
        return cur.fetchone() is not None
    except psycopg2.OperationalError:
        return False
    finally:
        cur.close()
        conn.close()


def drop_database(params, db_name):
    """Удаляет базу данных с заданным именем."""
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.close()
    conn.close()


def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    # Создаем подключение к базе данных по умолчанию
    default_params = config()
    conn = psycopg2.connect(**default_params)
    conn.autocommit = True

    # Создаем курсор для выполнения операций на уровне базы данных
    cur = conn.cursor()

    # Создаем базу данных с заданным именем, если она не существует
    cur.execute(f"CREATE DATABASE {db_name}")

    # Закрываем соединение
    cur.close()
    conn.close()


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""
    # Открываем файл с SQL-скриптом и читаем его содержимое
    with open(script_file, 'r') as file:
        sql_script = file.read()

    try:
        # Выполняем скрипт с помощью курсора
        cur.execute(sql_script)

        # Фиксируем изменения в базе данных с помощью коммита транзакции
        cur.connection.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при выполнении SQL-скрипта: {error}")
        # Откатываем транзакцию в случае ошибки
        cur.connection.rollback()
        raise  # Перехватываем ошибку и выводим ее для дальнейшего анализа


def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
    # SQL-запрос для создания таблицы suppliers
    sql_query = """
        CREATE TABLE suppliers (
            supplier_id SERIAL PRIMARY KEY,
            supplier_name VARCHAR(100),
            contact_name VARCHAR(100),
            contact_email VARCHAR(100),
            phone VARCHAR(20)
        )
    """
    # Выполняем SQL-запрос
    cur.execute(sql_query)


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла и возвращает список словарей с соответствующей информацией."""
    # Открываем файл с данными в формате JSON и загружаем его
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
    # SQL-запрос для вставки данных
    sql_query = """
        INSERT INTO suppliers (supplier_name, contact_name, contact_email, phone)
        VALUES (%s, %s, %s, %s)
    """
    # Вставляем данные из списка suppliers
    for supplier in suppliers:
        cur.execute(sql_query, (
            supplier['supplier_name'],
            supplier['contact_name'],
            supplier['contact_email'],
            supplier['phone']
        ))


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    # SQL-запрос для добавления внешнего ключа
    sql_query = """
        ALTER TABLE products
        ADD COLUMN supplier_id SERIAL,
        ADD FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
    """
    # Выполняем SQL-запрос
    cur.execute(sql_query)


if __name__ == '__main__':
    main()
