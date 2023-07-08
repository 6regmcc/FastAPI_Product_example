from fastapi import FastAPI, Response,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .import schemas
from .import models
from .database import engine, SessionLocal
from fastapi import status
from passlib.context import CryptContext
from .database import get_db
from .routers import product, seller


models.Base.metadata.create_all(engine)



app = FastAPI(
    title="Products API",
    description="Get details for all products",
    terms_of_service="www.example.com",

    license_info={
        "name": "xyc",
    },
    contact={
        "name": "xyc",
        "website": "example.com",
        "email": "6regmcc@gmail.com",
    },
)


app.include_router(product.router)
app.include_router(seller.router)








