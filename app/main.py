from fastapi import FastAPI 
from contextlib import asynccontextmanager 
 
from app.database import engine 
from app.models import Base 
from app.routers import auth, transactions, categories 
 
@asynccontextmanager 
async def lifespan(app: FastAPI): 
    print("Starting MoneyTracker API...") 
    print("Creating database tables...") 
    Base.metadata.create_all(bind=engine) 
    print("Database tables created!") 
    yield 
    print("Shutting down...") 
 
app = FastAPI(title="MoneyTracker API", version="1.0.0") 
 
app.include_router(auth.router) 
app.include_router(transactions.router) 
app.include_router(categories.router) 
 
@app.get("/") 
def read_root(): 
    return {"message": "Welcome to MoneyTracker API"} 
 
@app.get("/health") 
def health_check(): 
    return {"status": "healthy"} 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)