"""Точка запуска программы."""

import autopip

from models import Book, BookList, User
from models.status import ALL_STATUSES, get_status_display
from storage import load_books, load_users, save_books, save_users
from utils import input_int, input_non_empty, input_status


def show_book(book: Book) -> None:
    """Вывести информацию об одной книге."""
    print(f"  {book}")


def show_books(books: list) -> None:
    """Вывести список книг."""
    if not books:
        print("Список книг пуст.")
        return
    for book in books:
        show_book(book)


def show_all_books(book_list: BookList) -> None:
    """Вывести все книги пользователя."""
    print("\nВСЕ КНИГИ")
    show_books(book_list.books)
    print(" ")
    print(f"Всего книг: {len(book_list)}")


def show_books_by_status(book_list: BookList) -> None:
    """Вывести книги по выбранному статусу."""
    status = input_status("Выберите статус: ", ALL_STATUSES)
    filtered = book_list.filter_by_status(status)
    print(" ")
    print(f"КНИГИ СО СТАТУСОМ: {get_status_display(status)}")
    show_books(filtered)
    print(f"Всего: {len(filtered)}")


def search_books(book_list: BookList) -> None:
    """Поиск книг по подстроке."""
    query = input_non_empty("Введите название или автора: ")
    found = book_list.find(query)
    print(" ")
    print(f"РЕЗУЛЬТАТЫ ПОИСКА: {len(found)}")
    show_books(found)


def add_book_menu(book_list: BookList) -> None:
    """Добавить новую книгу."""
    print("\nДОБАВЛЕНИЕ КНИГИ")
    title = input_non_empty("Название: ")
    author = input_non_empty("Автор: ")
    year = input_int("Год издания: ")
    status = input_status("Выберите статус: ", ALL_STATUSES)

    error = Book.validate(title, author, year)
    if error:
        print(f"Ошибка: {error}")
        return

    book = Book(0, title, author, year, status)
    print(f"Книга \"{book.title}\" добавлена с ID {book.id}.")


def change_status_menu(book_list: BookList) -> None:
    """Изменить статус книги."""
    if not book_list.books:
        print("Список книг пуст.")
        return
    show_books(book_list.books)
    book_id = input_int("Введите ID книги: ")
    status = input_status("Выберите новый статус: ", ALL_STATUSES)
    if book_list.change_status(book_id, status):
        print("Статус изменен.")
    else:
        print("Книга не найдена.")


def remove_book_menu(book_list: BookList) -> None:
    """Удалить книгу."""
    if not book_list.books:
        print("Список книг пуст.")
        return
    show_books(book_list.books)
    book_id = input_int("Введите ID книги для удаления: ")
    removed = book_list.remove(book_id)
    if removed:
        print(f"Книга \"{removed.title}\" удалена.")
    else:
        print("Книга не найдена.")


def sort_books_menu(book_list: BookList) -> None:
    """Сортировка и вывод книг."""
    print("1. По названию")
    print("2. По году издания")
    choice = input_int("Выберите способ сортировки: ")
    if choice == 1:
        sorted_books = book_list.sort_by_title()
    elif choice == 2:
        sorted_books = book_list.sort_by_year()
    else:
        print("Неверный выбор.")
        return
    show_books(sorted_books)


def show_statistics(book_list: BookList) -> None:
    """Вывести статистику."""
    stats = book_list.get_statistics()
    print("\n" + "=" * 60)
    print("СТАТИСТИКА")
    print(" ")
    print(f"Пользователь: {book_list.user_name}")
    print(f"Всего книг: {stats['total']}")
    for status, count in stats["by_status"].items():
        print(f"  {get_status_display(status)}: {count}")
    print(f"Прогресс чтения: {stats['read_percent']:.1f}%")
    print(" ")


def show_menu(user_name: str) -> None:
    """Вывести главное меню."""
    print("\n СИСТЕМА УЧЕТА КНИГ ДЛЯ ЧТЕНИЯ")
    print(f"Пользователь: {user_name}")
    print(" ")
    print("1. Показать все книги")
    print("2. Показать книги по статусу")
    print("3. Найти книгу")
    print("4. Добавить книгу")
    print("5. Изменить статус книги")
    print("6. Удалить книгу")
    print("7. Сортировать книги")
    print("8. Статистика")
    print("0. Выход")


def main() -> None:
    """Точка входа программы."""
    users = load_users()
    if users:
        user = users[0]
    else:
        user = User(1, "Алена")
        users = [user]

    book_list = BookList(user.name)
    for book in load_books():
        book_list.add(book)

    print(f"Загружено книг: {len(book_list)}")

    while True:
        show_menu(user.name)
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_all_books(book_list)
        elif choice == "2":
            show_books_by_status(book_list)
        elif choice == "3":
            search_books(book_list)
        elif choice == "4":
            add_book_menu(book_list)
        elif choice == "5":
            change_status_menu(book_list)
        elif choice == "6":
            remove_book_menu(book_list)
        elif choice == "7":
            sort_books_menu(book_list)
        elif choice == "8":
            show_statistics(book_list)
        elif choice == "0":
            save_books(book_list.books)
            save_users(users)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
