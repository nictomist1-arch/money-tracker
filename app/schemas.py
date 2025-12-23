from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from enum import Enum


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

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