from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from models import Users, Task
from pydantic import BaseModel
from typing import Annotated
from .auth import get_current_user
from dependecis import db_dependency, bcrypt_context

router = APIRouter(
   prefix='/user',
   tags=['user']
)

class ChangePasswordRequest(BaseModel):
   password: str
   new_password: str

class createTakeReguest(BaseModel):
   title: str
   description: str
   priority: int

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/')
async def get_user_information(user: user_dependency, db: db_dependency):
   if user is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail='user not invalid')
   return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/info/change', status_code=status.HTTP_200_OK)
async def change_user_password(user: user_dependency,
                              db: db_dependency, var: ChangePasswordRequest):
   if user is None: 
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail='UNAUTHORIZED')
   user_model = db.query(Users).filter(Users.id == user.get('id')).first()

   if user_model is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail='user not found')
   if not bcrypt_context.verify(var.password, user_model.hashed_password):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                          detail='Error on change password')
   user_model.hashed_password = bcrypt_context.hash(var.new_password)
   db.add(user_model)
   db.commit()


@router.get('/tasks', status_code=status.HTTP_200_OK)
async def get_user_task(user: user_dependency, db: db_dependency):
   if user is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                          detail='login rirst')
   task_model = db.query(Task).filter(Task.owner_id == user.get('id')).all()
   return task_model


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_task_by_user(user: user_dependency,
                  db:db_dependency, requestBody: createTakeReguest):
   if user is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail='login first')
   task_model = Task(**requestBody.model_dump(), owner_id = user.get('id'))

   db.add(task_model)
   db.commit()