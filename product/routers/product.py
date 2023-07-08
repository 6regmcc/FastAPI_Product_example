from product.routers.login import get_current_user
from fastapi import FastAPI, Response,HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from ..import models
from typing import List
from ..import schemas

from fastapi import status

router = APIRouter(
    tags=["Product"],
    prefix="/product"
)


@router.post('/', response_model=schemas.DisplayProduct, status_code=status.HTTP_201_CREATED,)
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get('s/', response_model=List[schemas.DisplayProduct])
def products(db: Session = Depends(get_db), current_user: schemas.Seller = Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products


@router.get('/{id}')
def product(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")
    return product


@router.delete('/{id}')
def delete(id, response: Response, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)

    db.commit()
    return {"Product deleted"}


@router.put('/{id}')
def update(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    return {'product updated'}