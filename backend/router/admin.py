# adding change user role in admin panel

from fastapi import APIRouter, HTTPException, Depends, Path
from starlette import status
from models import Users, Task
from typing import Annotated
from pydantic import BaseModel
from .auth import get_current_user
from dependecis import db_dependency, bcrypt_context

router = APIRouter(
   prefix='/admin',
   tags=['admin']
)

class changeUserRole(BaseModel):
   role: str

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/tasks', status_code=status.HTTP_200_OK)
async def get_all_task_by_all_users(user: user_dependency, db: db_dependency):
   if user is None and user.get('role') != 'admin':
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail="Unauthentication")
   return db.query(Task).all()


@router.put('/users/role/{user_id}', status_code=status.HTTP_200_OK)
async def change_user_role(user: user_dependency, db: db_dependency, requestBody: changeUserRole, user_id: int = Path(gt=0)):
   if user is None and user.get('role') != 'admin':
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail="Unauthentication")
   user_to_change = db.query(Users).filter(Users.id == user_id).first()
   if not user_to_change:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail="User not found")
   user_to_change.role = requestBody.role
   db.add(user_to_change)
   db.commit()
   return {"message": f"User {user_to_change.username} role changed to {requestBody.role}"}