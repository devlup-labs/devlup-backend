from fastapi import FastAPI
from db.database import mentor_collection 
from routes.mentors_route import router as mentors_router

app= FastAPI()
app.include_router(mentors_router)

@app.get("/")
async def root():
   return {"message": "API working"}


