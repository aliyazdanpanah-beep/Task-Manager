# adding change user role in admin panel

from fastapi import APIRouter, HTTPException, Depends, Path
from starlette import status
from models import Users, Task
from typing import Annotated
from .auth import get_current_user
from dependecis import db_dependency, bcrypt_context

router = APIRouter(
   prefix='/admin',
   tags=['admin']
)

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/tasks', status_code=status.HTTP_200_OK)
async def get_all_task_by_all_users(user: user_dependency, db: db_dependency):
   if user is None and user.get('role') != 'admin':
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail="Unauthentication")
   return db.query(Task).all()