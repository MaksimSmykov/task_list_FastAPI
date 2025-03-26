from app.backend.db import SessionLocal

# Функция для получения сессии
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()