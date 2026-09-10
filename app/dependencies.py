from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
import jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.security import SECRET_KEY,ALGORITHM

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

def  get_token(token:str=Depends(oauth2_scheme)):
    return token

def get_current_user(
        token:str=Depends(oauth2_scheme),
        db:Session=Depends(get_db)
):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id=payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user=db.query(User).filter(
        User.id==user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="User not found"
        )

    return user