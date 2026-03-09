from fastapi import FastAPI
from routers import users

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Devlup backend running"}

app.include_router(users.router)