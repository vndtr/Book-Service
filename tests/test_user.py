
from user import (
    create_user,
    get_user_id,
    get_user_name,
    update_user_name,
)


def test_create_user():
    """Создание пользователя."""
    user = create_user(1, "Анна")
    assert user["id"] == 1
    assert user["name"] == "Анна"
    assert "created_at" in user


def test_get_user_name():
    """Получение имени."""
    user = create_user(1, "Анна")
    assert get_user_name(user) == "Анна"


def test_get_user_name_default():
    """Имя по умолчанию, если его нет."""
    assert get_user_name({}) == "Без имени"


def test_get_user_id():
    """Получение ID."""
    user = create_user(5, "Иван")
    assert get_user_id(user) == 5


def test_update_user_name():
    """Обновление имени."""
    user = create_user(1, "Анна")
    result = update_user_name(user, "Мария")
    assert result is True
    assert user["name"] == "Мария"


def test_update_user_name_empty():
    """Пустое имя не принимается."""
    user = create_user(1, "Анна")
    result = update_user_name(user, "   ")
    assert result is False
    assert user["name"] == "Анна"
