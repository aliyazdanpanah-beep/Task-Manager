from database import Base
from sqlalchemy import Integer, String, Boolean, Column, ForeignKey

class Users(Base):
   __tablename__ = 'users'

   id = Column(Integer, primary_key=True, index=True)
   email = Column(String, unique=True)
   username = Column(String)
   first_name = Column(String)
   last_name = Column(String)
   hashed_password = Column(String)
   is_active = Column(Boolean, default=True)
   role = Column(String, default='user')
   phone_number = Column(Integer)


class Task(Base):
   __tablename__ = 'task'

   id = Column(Integer, primary_key=True, index=True)
   title = Column(String)
   description = Column(String)
   priority = Column(Integer)
   owner_id = Column(Integer, ForeignKey('users.id'))