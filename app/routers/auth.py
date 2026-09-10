from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models import User
from app.schemas import UserCreate,UserResponse
from app.security import create_access_token
from app.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

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

@router.post("/login")
def login_user(
    form_data:OAuth2PasswordRequestForm=Depends(),
    db:Session=Depends(get_db)
):
    existing_user=db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    if not verify_password(
        form_data.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password"
        )
    access_token=create_access_token(
        data={"user_id":existing_user.id}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user:User=Depends(get_current_user)
):
    return {
        "id":current_user.id,
        "username":current_user.username
    }