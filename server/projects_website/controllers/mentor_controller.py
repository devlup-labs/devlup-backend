from fastapi import HTTPException
from bson import ObjectId
from server.core.database import mentor_collection
from server.projects_website.schemas.mentor_schema import Mentor

async def create_mentor_controller(mentor: Mentor):
    result = await mentor_collection.insert_one(mentor.model_dump())
    return {"mentor_id": str(result.inserted_id)}

async def get_mentor_controller(mentor_id: str):
    if not ObjectId.is_valid(mentor_id):
        raise HTTPException(status_code=400, detail="Invalid mentor ID")
        
    mentor = await mentor_collection.find_one({"_id": ObjectId(mentor_id)})
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
        
    mentor["id"] = str(mentor["_id"])
    del mentor["_id"]
    return mentor

async def update_mentor_controller(mentor_id: str, data: dict):
    if not ObjectId.is_valid(mentor_id):
        raise HTTPException(status_code=400, detail="Invalid mentor ID")
        
    update_result = await mentor_collection.update_one(
        {"_id": ObjectId(mentor_id)},
        {"$set": data}
    )
    
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Mentor not found")
        
    return {"message": "updated"}

async def delete_mentor_controller(mentor_id: str):
    if not ObjectId.is_valid(mentor_id):
        raise HTTPException(status_code=400, detail="Invalid mentor ID")
        
    delete_result = await mentor_collection.delete_one({"_id": ObjectId(mentor_id)})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Mentor not found")
        
    return {"message": "deleted"}

async def get_mentors_controller(year: int | None = None):
    query = {}
    if year:
        query["year"] = year

    mentors = []
    cursor = mentor_collection.find(query)

    async for m in cursor:
        m["id"] = str(m["_id"])
        del m["_id"]
        mentors.append(m)

    return mentors
