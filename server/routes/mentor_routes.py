from fastapi import APIRouter
from bson import ObjectId

from server.database import mentor_collection
from server.schemas.mentor_schema import Mentor
router = APIRouter()
@router.get("/mentors")
async def get_mentor():
    mentor =[]
    cursor = mentor_collection.find()
    async for a in cursor:
        a["_id"] =str(a["_id"])
        mentor.append(a)
    return mentor

# @router.get("/mentors")
# async def get_mentors(year: int | None = None):

#     query = {}

#     if year:
#         query["year"] = year

#     mentors = []

#     cursor = mentor_collection.find(query)

#     async for m in cursor:
#         m["_id"] = str(m["_id"])
#         mentors.append(m)

#     return mentors


# @router.post("/mentors")
# async def create_mentor(mentor: Mentor):

#     result = await mentor_collection.insert_one(mentor.dict())

#     return {"mentor_id": str(result.inserted_id)}


# @router.get("/mentors/{mentor_id}")
# async def get_mentor(mentor_id: str):

#     mentor = await mentor_collection.find_one({"_id": ObjectId(mentor_id)})
#     mentor["_id"] = str(mentor["_id"])

#     return mentor


# @router.put("/mentors/{mentor_id}")
# async def update_mentor(mentor_id: str, data: dict):

#     await mentor_collection.update_one(
#         {"_id": ObjectId(mentor_id)},
#         {"$set": data}
#     )

#     return {"message": "updated"}


# @router.delete("/mentors/{mentor_id}")
# async def delete_mentor(mentor_id: str):

#     await mentor_collection.delete_one({"_id": ObjectId(mentor_id)})

#     return {"message": "deleted"}