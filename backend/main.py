from fastapi import FastAPI, Path, Query, status
from dependecis import db_dependency
from models import Users

app = FastAPI()

@app.get('/')
async def get_all_tasks():
   return {'massage':'wellcom Task Manager'}


@app.get('/users')
async def get_all_users(db: db_dependency):
   return db.query(Users).all()