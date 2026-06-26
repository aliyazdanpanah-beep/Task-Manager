from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from passlib.context import CryptContext

def get_db() :
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')