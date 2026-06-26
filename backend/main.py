from fastapi import FastAPI, Path, Query, status
from router import auth

app = FastAPI()

app.include_router(auth.router)