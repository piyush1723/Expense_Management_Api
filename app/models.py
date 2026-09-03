from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(100),unique=True,nullable=False,index=True)
    hashed_password=Column(String(255),nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    categories=relationship("User",back_populates="user")

    incomes = relationship("Income", back_populates="user")

    expenses = relationship("Expense", back_populates="user")

class Category(Base):
    __tablename__="categories"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    user=relationship("User",back_populates="categories")
    expenses = relationship("Expense", back_populates="category")

class Income(Base):
    __tablename__="incomes"

    id=Column(Integer,primary_key=True,index=True)
    amount=Column(Numeric(10,2),nullable=False)
    source=Column(String(100),nullable=False)

    date=Column(DateTime,nullable=False)

    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    created_at=Column(DateTime(timezone=True),server_default=func.now())

    user=relationship("User",back_populates="incomes")
class Expense(Base):
    __tablename__="expenses"

    id=Column(Integer,primary_key=True,index=True)

    amount=Column(Numeric(10,2),nullable=False)
    description=Column(String(255),nullable=True)
    date=Column(DateTime,nullable=False)

    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    category_id=Column(Integer,ForeignKey("categories.id"),nullable=False)

    created_at=Column(DateTime(timezone=True),server_default=func.now())

    user=relationship("User",back_populates="expenses")
    category=relationship("Category",back_populates="expenses")