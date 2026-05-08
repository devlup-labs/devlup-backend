from fastapi import HTTPException
from bson import ObjectId
from server.database import timeline_collection
from server.schemas.timeline_schema import TimelineCreate, TimelineUpdate
from server.models.timeline_model import timeline_serializer

async def create_timeline_controller(timeline: TimelineCreate):
    timeline_dict = timeline.model_dump() if hasattr(timeline, "model_dump") else timeline.dict()
    result = await timeline_collection.insert_one(timeline_dict)
    return {"time_id": str(result.inserted_id)}

async def get_all_timelines_controller():
    timelines = []
    cursor = timeline_collection.find({})
    async for time_doc in cursor:
        timelines.append(timeline_serializer(time_doc))
    return timelines

async def get_timeline_controller(time_id: str):
    if not ObjectId.is_valid(time_id):
        raise HTTPException(status_code=400, detail="Invalid time ID")
        
    time_doc = await timeline_collection.find_one({"_id": ObjectId(time_id)})
    if not time_doc:
        raise HTTPException(status_code=404, detail="Timeline not found")
        
    return timeline_serializer(time_doc)

async def update_timeline_controller(time_id: str, data: TimelineUpdate):
    if not ObjectId.is_valid(time_id):
        raise HTTPException(status_code=400, detail="Invalid time ID")
        
    update_data_raw = data.model_dump() if hasattr(data, "model_dump") else data.dict()
    update_data = {k: v for k, v in update_data_raw.items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    update_result = await timeline_collection.update_one(
        {"_id": ObjectId(time_id)},
        {"$set": update_data}
    )
    
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Timeline not found")
        
    return {"message": "updated"}

async def delete_timeline_controller(time_id: str):
    if not ObjectId.is_valid(time_id):
        raise HTTPException(status_code=400, detail="Invalid time ID")
        
    delete_result = await timeline_collection.delete_one({"_id": ObjectId(time_id)})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Timeline not found")
        
    return {"message": "deleted"}
