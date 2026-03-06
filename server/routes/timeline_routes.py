from fastapi import APIRouter
from bson import ObjectId
from server.database import timeline_collection
from server.schemas.timeline_schema import Timeline

router = APIRouter()


@router.get("/timeline")
async def get_timeline():

    timeline = []

    cursor = timeline_collection.find()

    async for t in cursor:
        t["_id"] = str(t["_id"])
        timeline.append(t)

    return timeline


@router.post("/timeline")
async def create_timeline(data: Timeline):

    result = await timeline_collection.insert_one(data.dict())

    return {"time_id": str(result.inserted_id)}


@router.get("/timeline/{time_id}")
async def get_time(time_id: str):

    data = await timeline_collection.find_one({"_id": ObjectId(time_id)})
    data["_id"] = str(data["_id"])

    return data


@router.put("/timeline/{time_id}")
async def update_time(time_id: str, data: dict):

    await timeline_collection.update_one(
        {"_id": ObjectId(time_id)},
        {"$set": data}
    )

    return {"message": "updated"}


@router.delete("/timeline/{time_id}")
async def delete_time(time_id: str):

    await timeline_collection.delete_one({"_id": ObjectId(time_id)})

    return {"message": "deleted"}