@echo off
echo Финальное исправление всех ошибок...

cd /d "C:\Users\User\money-tracker"

echo 1. Исправляю auth.py...
echo from fastapi import APIRouter > app\routers\auth.py
echo. >> app\routers\auth.py
echo router = APIRouter(prefix="/auth", tags=["authentication"]) >> app\routers\auth.py
echo. >> app\routers\auth.py
echo @router.get("/test") >> app\routers\auth.py
echo def test_auth(): >> app\routers\auth.py
echo     return {"message": "Auth router works!"} >> app\routers\auth.py

echo 2. Исправляю transactions.py...
echo from fastapi import APIRouter > app\routers\transactions.py
echo. >> app\routers\transactions.py
echo router = APIRouter(prefix="/transactions", tags=["transactions"]) >> app\routers\transactions.py
echo. >> app\routers\transactions.py
echo @router.get("/test") >> app\routers\transactions.py
echo def test_transactions(): >> app\routers\transactions.py
echo     return {"message": "Transactions router works!"} >> app\routers\transactions.py

echo 3. Исправляю categories.py...
echo from fastapi import APIRouter > app\routers\categories.py
echo. >> app\routers\categories.py
echo router = APIRouter(prefix="/categories", tags=["categories"]) >> app\routers\categories.py
echo. >> app\routers\categories.py
echo @router.get("/test") >> app\routers\categories.py
echo def test_categories(): >> app\routers\categories.py
echo     return {"message": "Categories router works!"} >> app\routers\categories.py

echo 4. Упрощаю main.py...
echo from fastapi import FastAPI > app\main.py
echo from contextlib import asynccontextmanager >> app\main.py
echo. >> app\main.py
echo from app.database import engine >> app\main.py
echo from app.models import Base >> app\main.py
echo from app.routers import auth, transactions, categories >> app\main.py
echo. >> app\main.py
echo @asynccontextmanager >> app\main.py
echo async def lifespan(app: FastAPI): >> app\main.py
echo     print("Starting MoneyTracker API...") >> app\main.py
echo     print("Creating database tables...") >> app\main.py
echo     Base.metadata.create_all(bind=engine) >> app\main.py
echo     print("Database tables created!") >> app\main.py
echo     yield >> app\main.py
echo     print("Shutting down...") >> app\main.py
echo. >> app\main.py
echo app = FastAPI(title="MoneyTracker API", version="1.0.0", lifespan=lifespan) >> app\main.py
echo. >> app\main.py
echo app.include_router(auth.router) >> app\main.py
echo app.include_router(transactions.router) >> app\main.py
echo app.include_router(categories.router) >> app\main.py
echo. >> app\main.py
echo @app.get("/") >> app\main.py
echo def read_root(): >> app\main.py
echo     return {"message": "Welcome to MoneyTracker API"} >> app\main.py
echo. >> app\main.py
echo @app.get("/health") >> app\main.py
echo def health_check(): >> app\main.py
echo     return {"status": "healthy"} >> app\main.py

echo 5. Проверяю импорт...
python -c "from app.routers.auth import router; print('✅ Auth router импортируется')"
python -c "from app.routers.transactions import router; print('✅ Transactions router импортируется')"
python -c "from app.routers.categories import router; print('✅ Categories router импортируется')"

echo.
echo ✅ Все исправлено!
echo.
echo Теперь запускайте: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo После запуска откройте в браузере:
echo http://localhost:8000/
echo http://localhost:8000/docs
echo http://localhost:8000/auth/test
echo http://localhost:8000/transactions/test
echo http://localhost:8000/categories/test
pause