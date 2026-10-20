-- 1. Выборка всех книг (SELECT)
SELECT id, title, author, year FROM books ORDER BY title;

-- 2. Фильтрация по статусу (WHERE)
SELECT title, author FROM books WHERE status = 'прочитано';

-- 3. Фильтрация по диапазону (WHERE BETWEEN)
SELECT title, year FROM books WHERE year BETWEEN 1800 AND 1999;

-- 4. Поиск по тексту (WHERE LIKE)
SELECT title, author FROM books WHERE title LIKE '%мир%';

-- 5. Сортировка и ограничение (ORDER BY, LIMIT)
SELECT title, year FROM books ORDER BY year DESC LIMIT 3;

-- 6. Соединение таблиц: кто какие книги добавил (JOIN)
SELECT users.name AS user_name, books.title 
FROM books 
JOIN users ON books.user_id = users.id;

-- 7. Агрегатная функция: всего книг (COUNT)
SELECT COUNT(*) AS total_books FROM books;

-- 8. Агрегатная функция: средний год издания (AVG)
SELECT AVG(year) AS avg_year FROM books;

-- 9. Группировка: сколько книг в каждом статусе (GROUP BY, COUNT)
SELECT status, COUNT(*) AS count FROM books GROUP BY status;

-- 10. Фильтрация групп (HAVING) + JOIN
-- Книги, добавленные пользователем, у которого больше 5 книг
SELECT users.name, COUNT(books.id) AS books_count
FROM users
JOIN books ON users.id = books.user_id
GROUP BY users.id, users.name
HAVING COUNT(books.id) >= 5;