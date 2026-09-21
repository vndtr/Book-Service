from datetime import date


class User:
    """Пользователь системы учета книг."""

    def __init__(
        self,
        user_id: int,
        name: str,
        created_at: str = "",
    ) -> None:
        """Создать объект пользователя."""
        self.id: int = user_id
        self.name: str = name
        self.created_at: str = (
            created_at or date.today().strftime("%d.%m.%Y")
        )

    def update_name(self, new_name: str) -> bool:
        """Обновить имя пользователя."""
        if not new_name.strip():
            return False
        self.name = new_name.strip()
        return True

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Создать объект User из словаря."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            created_at=data.get("created_at", ""),
        )

    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return f"Пользователь: {self.name} (создан {self.created_at})"

    def __repr__(self) -> str:
        """Техническое представление пользователя."""
        return f"User({self.id}, {self.name!r})"
