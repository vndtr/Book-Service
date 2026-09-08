import datetime

STATUS_WANT_TO_READ = "хочу прочитать"
STATUS_READING = "читаю"
STATUS_READ = "прочитано"
STATUS_ON_HOLD = "отложено"


def get_status_display(status):
    if status == STATUS_READ:
        return "Прочитано"
    elif status == STATUS_READING:
        return "Читаю"
    elif status == STATUS_WANT_TO_READ:
        return "Хочу прочитать"
    elif status == STATUS_ON_HOLD:
        return "Отложено"
    else:
        return "Неизвестный статус"


user_name = "Анна"

book_title = "Война и мир"
book_author = "Лев Толстой"
book_year = 1869
book_status = STATUS_READING

print(f"Пользователь: {user_name}")
print(f"Книга: {book_title}")
print(f"Автор: {book_author}")
print(f"Год: {book_year}")
print(f"Статус: {get_status_display(book_status)}")

print("\nИзменить статус книги:")
print("1. Хочу прочитать")
print("2. Читаю")
print("3. Прочитано")
print("4. Отложено")

choice = input("Выберите новый статус (1-4): ")

if choice == "1":
    new_status = STATUS_WANT_TO_READ
elif choice == "2":
    new_status = STATUS_READING
elif choice == "3":
    new_status = STATUS_READ
elif choice == "4":
    new_status = STATUS_ON_HOLD
else:
    new_status = None

if new_status is not None:
    old_status = book_status
    book_status = new_status
    current_date = datetime.datetime.now()
    date_str = current_date.strftime("%d.%m.%Y")
    
    print(f"\nСтатус изменен: {get_status_display(old_status)} -> {get_status_display(book_status)}")
    print(f"Дата изменения: {date_str}")
else:
    print("Неверный выбор")