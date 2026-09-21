
from datetime import date


def create_user(user_id: int, name: str) -> dict:
    """Создать нового пользователя."""
    return {
        "id": user_id,
        "name": name,
        "created_at": date.today().strftime("%d.%m.%Y"),
    }


def get_user_name(user: dict) -> str:
    """Вернуть имя пользователя."""
    return user.get("name", "Без имени")


def get_user_id(user: dict) -> int:
    """Вернуть идентификатор пользователя."""
    return user.get("id", 0)


def update_user_name(user: dict, new_name: str) -> bool:
    """Обновить имя пользователя. Вернуть True при успехе."""
    if not new_name.strip():
        return False
    user["name"] = new_name.strip()
    return True
