@echo off
echo Исправление проблем с кодировкой базы данных...

cd /d "C:\Users\User\money-tracker"

REM 1. Удаляем старый файл базы
del money_tracker.db 2>nul

REM 2. Создаем новый database.py
echo from sqlalchemy import create_engine > app\database.py
echo from sqlalchemy.ext.declarative import declarative_base >> app\database.py
echo from sqlalchemy.orm import sessionmaker >> app\database.py
echo. >> app\database.py
echo # Простой путь для SQLite на Windows >> app\database.py
echo engine = create_engine("sqlite:///money_tracker.db", connect_args={"check_same_thread": False}) >> app\database.py
echo SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) >> app\database.py
echo Base = declarative_base() >> app\database.py
echo. >> app\database.py
echo def get_db(): >> app\database.py
echo     db = SessionLocal() >> app\database.py
echo     try: >> app\database.py
echo         yield db >> app\database.py
echo     finally: >> app\database.py
echo         db.close() >> app\database.py

echo ✅ app/database.py обновлен
echo.

REM 3. Проверяем базу данных
echo import sqlite3 > test_db.py
echo. >> test_db.py
echo try: >> test_db.py
echo     conn = sqlite3.connect("money_tracker.db") >> test_db.py
echo     print("SQLite подключение работает!") >> test_db.py
echo     conn.close() >> test_db.py
echo except Exception as e: >> test_db.py
echo     print(f"Ошибка: {e}") >> test_db.py

echo Проверяем SQLite...
python test_db.py

echo.
echo Теперь запускайте: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause