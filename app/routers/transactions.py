from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timedelta
from app.database import get_db
from app.auth import get_current_user
from app import models, schemas

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_data: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Создать новую транзакцию (доход или расход).
    Логика: проверить существование категории, создать запись.
    """
    # 1. Проверить, что категория существует и принадлежит пользователю
    category = db.query(models.Category).filter(
        models.Category.id == transaction_data.category_id,
        models.Category.user_id == current_user.id
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found or access denied"
        )

    # 2. Создать объект транзакции
    db_transaction = models.Transaction(
        **transaction_data.dict(),
        user_id=current_user.id
    )

    # 3. Сохранить в базу
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=List[schemas.TransactionResponse])
def get_transactions(
    start_date: Optional[date] = Query(None, description="Фильтр: с даты"),
    end_date: Optional[date] = Query(None, description="Фильтр: по дату"),
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Получить список транзакций с фильтрацией по дате и категории.
    """
    query = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id)

    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    if category_id:
        query = query.filter(models.Transaction.category_id == category_id)

    transactions = query.order_by(models.Transaction.date.desc()).offset(skip).limit(limit).all()
    return transactions

@router.get("/stats/current-month")
def get_current_month_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Получить статистику по доходам/расходам за текущий месяц.
    Бизнес-логика: вычисление суммы по типам транзакций.
    """
    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)

    # Запросы к базе данных для агрегации
    income = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.date >= first_day_of_month,
        models.Transaction.date <= today,
        models.Category.type == models.TransactionType.INCOME  # Предполагается JOIN с Category
    ).scalar() or 0.0

    expense = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == current_user.id,
        models.Transaction.date >= first_day_of_month,
        models.Transaction.date <= today,
        models.Category.type == models.TransactionType.EXPENSE  # Предполагается JOIN с Category
    ).scalar() or 0.0

    return {
        "period": f"{first_day_of_month.isoformat()} - {today.isoformat()}",
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense
    }
