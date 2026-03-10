from sqlalchemy.orm import Session
from database import SessionLocal
from models import Todo


def seed_todos():
    db = SessionLocal()

    todos_data = [
        {"title": "Kupić mleko", "description": "Przez niedzielą", "is_completed": False, "priority": 2, "owner_id": 1},
        {"title": "Zrobić pranie", "description": "Pranie kolorów i bieli", "is_completed": True, "priority": 1,
         "owner_id": 1},
        {"title": "Wysłać CV", "description": "Aplikacja na nową pracę", "is_completed": False, "priority": 4,
         "owner_id": 1},

        # Todos dla ID 2
        {"title": "Odebrać paczkę", "description": "Paczka w Paczkomacie przy sklepie", "is_completed": False,
         "priority": 3, "owner_id": 2},
        {"title": "Umyć samochód", "description": "Myjnia na Stawowej", "is_completed": True, "priority": 2,
         "owner_id": 2},
        {"title": "Zadzwonić do mechanika", "description": "Umówić się na przegląd", "is_completed": False,
         "priority": 3, "owner_id": 2},

        # Admin ID 3 - tylko 1 todo
        {"title": "Przygotować raport admina", "description": "Raport miesięczny dla zarządu", "is_completed": False,
         "priority": 5, "owner_id": 3},

        # Todos dla ID 4
        {"title": "Kupić prezent", "description": "Prezent dla mamy na urodziny", "is_completed": False, "priority": 4,
         "owner_id": 4},
        {"title": "Posprzątać mieszkanie", "description": "Ogólne porządki", "is_completed": True, "priority": 2,
         "owner_id": 4},
        {"title": "Zrobić zakupy spożywcze", "description": "Chleb, mleko, jajka, masło", "is_completed": False,
         "priority": 2, "owner_id": 4},
        {"title": "Odwiedzić babcię", "description": "Wpadnij do babci w niedzielę", "is_completed": False,
         "priority": 3, "owner_id": 4},

        # Todos dla ID 5
        {"title": "Nauczyć się FastAPI", "description": "Kurs na YouTube i dokumentacja", "is_completed": False,
         "priority": 5, "owner_id": 5},
        {"title": "Zrobić projekt", "description": "Projekt zaliczeniowy na studia", "is_completed": True,
         "priority": 4, "owner_id": 5},
        {"title": "Kupić bilet do kina", "description": "Nowy film z DiCaprio", "is_completed": False, "priority": 1,
         "owner_id": 5},
        {"title": "Zarezerwować stolik", "description": "Kolacja z dziewczyną w sobotę", "is_completed": False,
         "priority": 3, "owner_id": 5},
    ]

    try:
        for todo_data in todos_data:
            todo = Todo(**todo_data)
            db.add(todo)
        db.commit()
        print("✅ Todosy zostały dodane pomyślnie!")
    except Exception as e:
        db.rollback()
        print(f"❌ Błąd: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_todos()