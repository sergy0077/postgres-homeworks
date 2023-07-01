"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="north",
    user="postgres",
    password="130468"
)
cur = conn.cursor()

"""заполнение таблиц данными"""
with open("C:/Users/Sergy007/PycharmProjects/postgres-homeworks/homework-1/north_data/customers_data.csv", 'r') as file:
    next(file)
    for line in file:
        data = line.strip().split(',')
        cur.execute("INSERT INTO customers (customer_id, company_name, contact_name) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (data[0], data[1], data[2]))

with open("C:/Users/Sergy007/PycharmProjects/postgres-homeworks/homework-1/north_data/employees_data.csv", 'r') as file:
    next(file)
    for line in file:
        data = line.strip().split(',')
        cur.execute("INSERT INTO employees (employee_id, first_name, last_name, title, birth_date, notes) VALUES "
            "(%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", (data[0], data[1], data[2], data[3], data[4], data[5]))

with open("C:/Users/Sergy007/PycharmProjects/postgres-homeworks/homework-1/north_data/orders_data.csv", 'r') as file:
    next(file)
    for line in file:
        data = line.strip().split(',')
        cur.execute("INSERT INTO orders (order_id, customer_id, employee_id, order_date, ship_city) VALUES "
                    "(%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", (data[0], data[1], data[2], data[3], data[4]))

conn.commit()

"""проверка данных, запасанных в таблицы"""
cur.execute("SELECT * FROM employees")
print(cur.fetchall())

cur.execute("SELECT * FROM customers")
print(cur.fetchall())

cur.execute("SELECT * FROM orders")
print(cur.fetchall())

cur.close()
conn.close()
