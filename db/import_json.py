import json
from db.database import get_connection

USERS_FILE = "data/users.json"
BOOKS_FILE = "data/books.json"

def load_json(filename):
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def import_users(conn):
    users = load_json(USERS_FILE)
    if not users:
        return
    conn.executemany(
        "INSERT INTO users (id, name, created_at) VALUES (?, ?, ?)",
        [(u["id"], u["name"], u.get("created_at", "")) for u in users]
    )

def import_books(conn):
    books = load_json(BOOKS_FILE)
    if not books:
        return
    
    # Для связи привяжем все книги к первому пользователю (user_id = 1)
    default_user_id = 1 
    
    conn.executemany(
        """
        INSERT INTO books (id, title, author, year, status, date_added, user_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                b["id"], b["title"], b["author"], b["year"], 
                b["status"], b.get("date_added", ""), default_user_id
            ) 
            for b in books
        ]
    )

def main():
    conn = get_connection()
    try:
        import_users(conn)
        import_books(conn)
        conn.commit()
        print("Данные успешно импортированы.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка импорта: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()