from fastapi import FastAPI, Path, Query, status
from router import auth, user, admin

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)