from __future__ import annotations  # Должно быть первой строкой
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

# ===== Enums =====
class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

# ===== User Schemas =====
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    # УБРАЛИ циклическую ссылку на транзакции здесь
    # transactions: List['TransactionResponse']  
    
    model_config = ConfigDict(from_attributes=True)

# ===== Category Schemas =====
class CategoryBase(BaseModel):
    name: str
    type: TransactionType

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    user_id: int
    # Заменили циклическую ссылку на простой ID
    parent_category_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

# ===== Transaction Schemas =====
class TransactionBase(BaseModel):
    amount: float
    date: date = Field(default_factory=date.today)
    description: Optional[str] = None
    category_id: int

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    date: Optional[date] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ===== Other Schemas (если нужны) =====
class DashboardStats(BaseModel):
    total_income: float = 0.0
    total_expenses: float = 0.0
    balance: float = 0.0
    monthly_expenses_by_category: dict = {}
    
    model_config = ConfigDict(from_attributes=True)