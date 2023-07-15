-- Подключиться к БД Northwind и сделать следующие изменения:
-- 1. Добавить ограничение на поле unit_price таблицы products (цена должна быть больше 0)
ALTER TABLE products
ADD CONSTRAINT positive_unit_price CHECK (unit_price > 0);


-- 2. Добавить ограничение, что поле discontinued таблицы products может содержать только значения 0 или 1
ALTER TABLE products
ADD CONSTRAINT check_discontinued_values CHECK (discontinued IN (0, 1));


-- 3. Создать новую таблицу, содержащую все продукты, снятые с продажи (discontinued = 1)
CREATE TABLE discontinued_products AS
SELECT *
FROM products
WHERE discontinued = 1;


-- 4. Удалить из products товары, снятые с продажи (discontinued = 1)

-- создаем временную таблицу с товарами, которые не являются снятыми с продажи
CREATE TABLE tmp_products AS
SELECT *
FROM products
WHERE discontinued = 0;

-- удаляем ограничения foreign key временно
ALTER TABLE order_details
DROP CONSTRAINT fk_orderdetails_productid;

 -- удаляем связанные кортежи в таблице order_details
DELETE FROM order_details
WHERE product_id IN (
  SELECT product_id
  FROM products
  WHERE discontinued = 1
);

-- очищаем таблицу "products":
TRUNCATE TABLE products CASCADE;

--восстановливаем данные из временной таблицы в таблицу "products":
INSERT INTO products
SELECT tp.*
FROM tmp_products tp;

-- восстановливаем ограничения foreign key
ALTER TABLE order_details
ADD CONSTRAINT fk_orderdetails_productid
FOREIGN KEY (product_id) REFERENCES products (product_id);
