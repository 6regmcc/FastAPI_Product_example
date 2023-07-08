from fastapi import FastAPI, Response,HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from ..import models
from typing import List
from ..import schemas
from passlib.context import CryptContext

from fastapi import status

router = APIRouter(
    tags=["Seller"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/seller', response_model=schemas.DisplaySeller, status_code=status.HTTP_201_CREATED)
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username,email=request.email,password=hashed_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
