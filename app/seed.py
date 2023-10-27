from app.database import get_db
from app.crud import add_item

def run():
    try:
        
        print("Seeding")
        db = get_db()
    except Exception as e:
        print(e)
        print("Failed to connect to database")
        return
    # add_item(db, {"quantity": 10})

if __name__ == '__main__':
    run()