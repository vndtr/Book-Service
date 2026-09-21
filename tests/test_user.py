
from models.user import User


def test_create_user():
    """Создание пользователя."""
    user = User(1, "Анна")
    assert user.id == 1
    assert user.name == "Анна"
    assert user.created_at != ""


def test_update_user_name():
    """Обновление имени."""
    user = User(1, "Анна")
    assert user.update_name("Мария") is True
    assert user.name == "Мария"


def test_update_user_name_empty():
    """Пустое имя не принимается."""
    user = User(1, "Анна")
    assert user.update_name("   ") is False
    assert user.name == "Анна"


def test_user_str():
    """Строковое представление."""
    user = User(1, "Анна")
    assert "Анна" in str(user)


def test_user_to_dict():
    """Преобразование в словарь."""
    user = User(1, "Анна", "01.09.2026")
    data = user.to_dict()
    assert data["id"] == 1
    assert data["name"] == "Анна"
    assert data["created_at"] == "01.09.2026"


def test_user_from_dict():
    """Создание из словаря."""
    data = {"id": 1, "name": "Анна", "created_at": "01.09.2026"}
    user = User.from_dict(data)
    assert user.id == 1
    assert user.name == "Анна"
