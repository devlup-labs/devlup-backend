from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from server.database import application_collection
from server.schemas.application_schema import ApplicationCreate, ApplicationUpdate

async def get_applications_controller():
    applications = []
    cursor = application_collection.find()
    
    async for a in cursor:
        a["id"] = str(a["_id"])
        del a["_id"]
        applications.append(a)
        
    return applications

async def create_application_controller(application: ApplicationCreate):
    app_dict = application.dict()
    app_dict["created_at"] = datetime.utcnow()
    
    result = await application_collection.insert_one(app_dict)
    
    new_app = await application_collection.find_one({"_id": result.inserted_id})
    new_app["id"] = str(new_app["_id"])
    del new_app["_id"]
    
    return new_app

async def get_application_controller(application_id: str):
    if not ObjectId.is_valid(application_id):
        raise HTTPException(status_code=400, detail="Invalid application ID")
        
    app = await application_collection.find_one({"_id": ObjectId(application_id)})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    app["id"] = str(app["_id"])
    del app["_id"]
    
    return app

async def update_application_controller(application_id: str, application_update: ApplicationUpdate):
    if not ObjectId.is_valid(application_id):
        raise HTTPException(status_code=400, detail="Invalid application ID")
        
    update_data = {k: v for k, v in application_update.dict().items() if v is not None}
    
    if len(update_data) >= 1:
        update_result = await application_collection.update_one(
            {"_id": ObjectId(application_id)}, {"$set": update_data}
        )
        if update_result.modified_count == 0 and update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Application not found")
            
    app = await application_collection.find_one({"_id": ObjectId(application_id)})
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    app["id"] = str(app["_id"])
    del app["_id"]
    
    return app

async def delete_application_controller(application_id: str):
    if not ObjectId.is_valid(application_id):
        raise HTTPException(status_code=400, detail="Invalid application ID")
        
    delete_result = await application_collection.delete_one({"_id": ObjectId(application_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Application not found")
        
    return {"message": "deleted"}
