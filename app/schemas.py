from pydantic import BaseModel,Field
from datetime import datetime

class UserCreate(BaseModel):
    username:str=Field(min_length=3,max_length=100)
    password:str=Field(min_length=6,max_length=100)

class UserResponse(BaseModel):
    id:int
    username:str

class CategoryCreate(BaseModel):
    name:str=Field(min_length=2,max_length=100)

class CategoryResponse(BaseModel):
    id:int
    name:str

class IncomeCreate(BaseModel):
    amount:float=Field(gt=0)
    source:str=Field(min_length=2,max_length=100)
    date:datetime

class IncomeResponse(BaseModel):
    id: int
    amount: float
    source: str
    date: datetime

class ExpenseCreate(BaseModel):
    amount:float=Field(gt=0)
    description:str | None=Field(default=None,max_length=255)
    date:datetime
    category_id:int

class ExpenseResponse(BaseModel):
    id:int
    amount:float
    description:str|None
    date:datetime
    category_id:int

