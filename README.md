# Book Service – система учета книг для чтения

## Назначение
Book Service – веб-приложение на Django для учета книг, которые пользователь читает, планирует прочитать или уже прочитал. Консольная версия (ПР3) сохранена. Данные веб-версии хранятся в базе SQLite и обрабатываются через Django ORM.

## Технологии
* Python 3, Django 5.2, SQLite, Django ORM;
* Django Admin и Django Debug Toolbar;
* Django Forms (Form, ModelForm), загрузка изображений (Pillow);
* Unidecode – транслитерация названий для slug;
* HTML, Bootstrap 5.3, CSS;
* pytest и тесты Django, flake8.

## Возможности
* список книг `/books/` – форма фильтрации (статус, годы издания, пользователь), сортировка, пагинация по 5 книг, параметры сохраняются в ссылках страниц;
* страница книги `/books/<slug>/` – подробности, обложка, смена статуса, кнопки «Редактировать» и «Отложить»;
* добавление `/books/create/` и редактирование `/books/<id>/edit/` книги через ModelForm, загрузка обложки;
* «Отложить» книгу (`/books/<id>/hold/`, только POST) – меняется статус, запись остается в базе;
* поиск `/books/search/` (название, автор, имя пользователя; без учета регистра, в том числе для кириллицы);
* статистика `/books/stats/` – агрегаты `Count` с условиями `Q` по статусам, годы издания, книги по пользователям;
* административная панель `/admin/`;
* общие данные во всех шаблонах (контекстный процессор): название сайта и число книг в навигации.

## Модели
* **User** (`users/models.py`) – `name`, `created_at`.
* **Book** (`books/models.py`) – `title`, `author`, `year`, `status`, `date_added`, `user` (`ForeignKey`, `PROTECT`, `related_name="books"`), `slug`, `cover`, `is_classic`.

Статусы описаны перечислением `Book.Status` (`TextChoices`): `want_to_read` – «Хочу прочитать» (по умолчанию), `reading` – «Читаю», `read` – «Прочитано», `on_hold` – «Отложено».

Особенности модели Book:
* `BookQuerySet` и `BookManager`: `Book.objects.active()` (все, кроме отложенных), `want_to_read()`, `reading()`, `read()`, `on_hold()`; условия отбора вынесены из представлений в модель;
* `slug` – `SlugField(unique=True, editable=False)`: формируется при первом сохранении из транслитерации названия и первичного ключа (например, `voina-i-mir-1`);
* `get_absolute_url()` возвращает адрес страницы через `reverse("books:detail", ...)`; используется в шаблонах и в ссылке «Посмотреть на сайте» в админке;
* `is_classic` – `GeneratedField(db_persist=True)`: база данных сама вычисляет признак «издана до 1950 года» по полю `year`;
* `put_on_hold()` – «отмена» книги: статус меняется на `on_hold`, запись не удаляется;
* `cover` – `ImageField(upload_to="covers/")`, файлы хранятся в `media/covers/`.

## Миграции (`books/migrations/`)
| Файл | Назначение |
|---|---|
| `0001_initial` | таблица книг |
| `0002_migrate_status_codes` | миграция данных: русские названия статусов → коды `TextChoices` (с обратным преобразованием) |
| `0003_alter_book_status` | поле `status` получает `choices` и новое значение по умолчанию |
| `0004_book_slug` | добавление поля `slug` |
| `0005_populate_book_slugs` | миграция данных: заполнение `slug` для существующих книг |
| `0006_book_slug_unique` | ограничение уникальности `slug` |
| `0007_book_is_classic_help_texts` | вычисляемое поле `is_classic`, подписи и подсказки полей |
| `0008_book_cover` | поле `cover` |

В `users/migrations/0002_alter_user_options` зафиксирована сортировка пользователей по имени.

## Django Admin
* **BookAdmin** – столбцы, поиск по названию, автору и `user__name`, фильтры (статус, классика, год, пользователь), сортировка, 20 записей на странице, `list_editable` для статуса, `list_select_related`, `autocomplete_fields`, поля только для чтения (`id`, `slug`, `is_classic`), `view_on_site`, столбец «Страница на сайте», массовые действия «Отложить выбранные книги» и «Вернуть в “Хочу прочитать”»;
* **UserAdmin** – поиск по имени, число активных книг (аннотация `Count` в `get_queryset()`), встроенная таблица книг `BookInline` в карточке пользователя;
* русские названия приложений (`verbose_name` в `AppConfig`), моделей и полей.

Административная панель не заменяет бизнес-правила: проверка дубликатов выполняется в формах и представлениях сайта, а не в админке.

## Формы (`books/forms.py`)
* `BookFilterForm` (`forms.Form`) – GET-параметры `status`, `year_from`, `year_to`, `user`, `sort`; проверка типов, существования пользователя, допустимых значений сортировки и диапазона годов в `clean()`;
* `BookForm` (`forms.ModelForm`) – поля `title`, `author`, `year`, `user`, `cover`; статус, slug и дата добавления пользователем не задаются; подписи, подсказки, виджеты Bootstrap; проверки: валидатор-функция `validate_year_range`, `clean_title()`, `clean_author()`, `clean_year()` (год не в будущем), `clean_cover()` (до 2 МБ);
* правило предметной области: у одного пользователя не может быть двух активных книг с одинаковыми названием и автором. Проверка выполняется в представлениях (`Book.objects.active()...exists()`); при редактировании текущая книга исключается через `exclude(pk=book.pk)`. Отложенная книга новую такую же не блокирует.

Все изменяющие операции выполняются POST-запросами с `{% csrf_token %}`; несуществующие объекты возвращают 404 (`get_object_or_404`).

## Хранение данных
Данные веб-версии – `db.sqlite3` (в репозиторий не входит). Исходная база ПР7 `data/library.sqlite` используется только как источник для `db/import_to_orm.py`. Загруженные обложки хранятся в каталоге `media/` (в репозиторий не входит).

## Запуск
```text
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python db/import_to_orm.py      (только для новой базы: перенос данных ПР7)
python manage.py createsuperuser
python manage.py runserver
```
Сайт: `http://127.0.0.1:8000/`, админка: `http://127.0.0.1:8000/admin/`. Django Debug Toolbar отображается при `DEBUG = True` на локальном адресе.

Консольная версия: `python main.py`.

## Проверка
```text
python manage.py check
python manage.py makemigrations --check
python manage.py test
pytest -v
flake8 . --extend-exclude=.venv
```

## Структура проекта
```text
Book Service/
├── manage.py, main.py, storage.py, utils.py, requirements.txt
├── book_service/   – настройки, корневые маршруты, MEDIA, debug toolbar
├── homepage/       – главная страница, страница 404, статика
├── users/          – модель User, админка с inline книг
├── books/          – модель Book, QuerySet, формы, представления, шаблоны,
│                     контекстный процессор, админка, миграции, тесты
├── templates/      – base.html, 404.html, навигация
├── models/         – классы предметной области ПР3 (консольная версия)
├── db/, sql/       – скрипты и SQL ПР7, перенос данных в ORM
├── data/           – JSON и исходная база library.sqlite
├── tests/          – тесты консольной версии (pytest)
└── media/          – загруженные обложки (не в Git)
```

## Автор
Селезнева Алёна, группа ЭФБО-01-24.
