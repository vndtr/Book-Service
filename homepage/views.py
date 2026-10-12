from django.http import HttpResponse


def page(title, content):
    """Собрать HTML-страницу: общий каркас, Bootstrap и навигация."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/books/">Книги</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница: описание приложения и навигация."""
    content = """
    <h1 class="display-4">Book Service</h1>
    <p class="lead">Система учета книг для чтения.</p>
    <p>Основные разделы:</p>
    <a href="/books/" class="btn btn-primary me-2">Книги</a>
    """
    return HttpResponse(page("Book Service", content))


def page_not_found(request, exception):
    """Собственная страница ошибки 404 (используется в handler404)."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
