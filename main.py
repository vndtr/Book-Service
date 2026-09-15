"""Точка запуска программы."""

from books import (
    ALL_STATUSES,
    STATUS_READ,
    STATUS_READING,
    STATUS_WANT_TO_READ,
    STATUS_ON_HOLD,
    add_book,
    change_status,
    filter_books_by_status,
    find_books,
    get_statistics,
    get_status_display,
    remove_book,
    sort_books_by_title,
    sort_books_by_year,
)
from storage import load_books, save_books
from utils import input_int, input_non_empty, input_status

USER_NAME = "Алена"


def show_book(book: dict) -> None:
    """Вывести информацию об одной книге."""
    status = get_status_display(book["status"])
    print(f"  [{book['id']}] \"{book['title']}\" — {book['author']} "
          f"({book['year']}) | Статус: {status}")


def show_books(books: list) -> None:
    """Вывести список книг."""
    if not books:
        print("Список книг пуст.")
        return
    for book in books:
        show_book(book)


def show_all_books(books: list) -> None:
    """Вывести все книги пользователя."""
    print("\nВСЕ КНИГИ")
    show_books(books)
    print(" ")
    print(f"Всего книг: {len(books)}")


def show_books_by_status(books: list) -> None:
    """Вывести книги по выбранному статусу."""
    status = input_status("Выберите статус: ", ALL_STATUSES)
    filtered = filter_books_by_status(books, status)
    print(" ")
    print(f"КНИГИ СО СТАТУСОМ: {get_status_display(status)}")
    show_books(filtered)
    print(f"Всего: {len(filtered)}")


def search_books(books: list) -> None:
    """Поиск книг по подстроке."""
    query = input_non_empty("Введите название или автора: ")
    found = find_books(books, query)
    print(" ")
    print(f"РЕЗУЛЬТАТЫ ПОИСКА: {len(found)}")
    show_books(found)


def add_book_menu(books: list) -> None:
    """Добавить новую книгу."""
    print("\nДОБАВЛЕНИЕ КНИГИ")
    title = input_non_empty("Название: ")
    author = input_non_empty("Автор: ")
    year = input_int("Год издания: ")
    status = input_status("Выберите статус: ", ALL_STATUSES)
    book = add_book(books, title, author, year, status)
    print(f"Книга \"{book['title']}\" добавлена с ID {book['id']}.")


def change_status_menu(books: list) -> None:
    """Изменить статус книги."""
    if not books:
        print("Список книг пуст.")
        return
    show_books(books)
    book_id = input_int("Введите ID книги: ")
    status = input_status("Выберите новый статус: ", ALL_STATUSES)
    if change_status(books, book_id, status):
        print("Статус изменен.")
    else:
        print("Книга не найдена.")


def remove_book_menu(books: list) -> None:
    """Удалить книгу."""
    if not books:
        print("Список книг пуст.")
        return
    show_books(books)
    book_id = input_int("Введите ID книги для удаления: ")
    removed = remove_book(books, book_id)
    if removed:
        print(f"Книга \"{removed['title']}\" удалена.")
    else:
        print("Книга не найдена.")


def sort_books_menu(books: list) -> None:
    """Сортировка и вывод книг."""
    print("1. По названию")
    print("2. По году издания")
    choice = input_int("Выберите способ сортировки: ")
    if choice == 1:
        sorted_books = sort_books_by_title(books)
    elif choice == 2:
        sorted_books = sort_books_by_year(books)
    else:
        print("Неверный выбор.")
        return
    show_books(sorted_books)


def show_statistics(books: list) -> None:
    """Вывести статистику."""
    stats = get_statistics(books)
    print("\n" + "=" * 60)
    print("СТАТИСТИКА")
    print("=" * 60)
    print(f"Пользователь: {USER_NAME}")
    print(f"Всего книг: {stats['total']}")
    for status, count in stats["by_status"].items():
        print(f"  {get_status_display(status)}: {count}")
    print(f"Прогресс чтения: {stats['read_percent']:.1f}%")
    print("=" * 60)


def show_menu() -> None:
    """Вывести главное меню."""
    print("\n СИСТЕМА УЧЕТА КНИГ ДЛЯ ЧТЕНИЯ")
    print(f"Пользователь: {USER_NAME}")
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
    books = load_books()
    print(f"Загружено книг: {len(books)}")

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_all_books(books)
        elif choice == "2":
            show_books_by_status(books)
        elif choice == "3":
            search_books(books)
        elif choice == "4":
            add_book_menu(books)
        elif choice == "5":
            change_status_menu(books)
        elif choice == "6":
            remove_book_menu(books)
        elif choice == "7":
            sort_books_menu(books)
        elif choice == "8":
            show_statistics(books)
        elif choice == "0":
            save_books(books)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()