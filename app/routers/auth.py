from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models import User
from app.schemas import UserCreate,UserResponse

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(user:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    hashed_password=hash_password(user.password)

    new_user=User(
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user