from fastapi import FastAPI, Path, Query, status

app = FastAPI()

@app.get('/')
async def get_all_tasks():
   return {'massage':'wellcom Task Manager'}