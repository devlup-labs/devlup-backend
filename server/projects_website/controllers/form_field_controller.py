from fastapi import HTTPException
from bson import ObjectId
from server.core.database import form_fields_collection
from server.projects_website.schemas.form_field_schema import FormFieldCreate, FormFieldUpdate

async def get_form_fields_controller():
    fields = []
    cursor = form_fields_collection.find().sort("order", 1)
    
    async for f in cursor:
        f["id"] = str(f["_id"])
        del f["_id"]
        fields.append(f)
        
    return fields

async def create_form_field_controller(field: FormFieldCreate):
    field_dict = field.dict()
    
    # Check if a field with this name already exists
    existing_field = await form_fields_collection.find_one({"name": field.name})
    if existing_field:
        raise HTTPException(status_code=400, detail="A form field with this name already exists")
    
    result = await form_fields_collection.insert_one(field_dict)
    
    new_field = await form_fields_collection.find_one({"_id": result.inserted_id})
    new_field["id"] = str(new_field["_id"])
    del new_field["_id"]
    
    return new_field

async def get_form_field_controller(field_id: str):
    if not ObjectId.is_valid(field_id):
        raise HTTPException(status_code=400, detail="Invalid field ID")
        
    field = await form_fields_collection.find_one({"_id": ObjectId(field_id)})
    if not field:
        raise HTTPException(status_code=404, detail="Form field not found")
        
    field["id"] = str(field["_id"])
    del field["_id"]
    
    return field

async def update_form_field_controller(field_id: str, field_update: FormFieldUpdate):
    if not ObjectId.is_valid(field_id):
        raise HTTPException(status_code=400, detail="Invalid field ID")
        
    update_data = {k: v for k, v in field_update.dict().items() if v is not None}
    
    if "name" in update_data:
        existing_field = await form_fields_collection.find_one({
            "name": update_data["name"],
            "_id": {"$ne": ObjectId(field_id)}
        })
        if existing_field:
            raise HTTPException(status_code=400, detail="A form field with this name already exists")
    
    if len(update_data) >= 1:
        update_result = await form_fields_collection.update_one(
            {"_id": ObjectId(field_id)}, {"$set": update_data}
        )
        if update_result.modified_count == 0 and update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Form field not found")
            
    field = await form_fields_collection.find_one({"_id": ObjectId(field_id)})
    if not field:
        raise HTTPException(status_code=404, detail="Form field not found")
        
    field["id"] = str(field["_id"])
    del field["_id"]
    
    return field

async def delete_form_field_controller(field_id: str):
    if not ObjectId.is_valid(field_id):
        raise HTTPException(status_code=400, detail="Invalid field ID")
        
    delete_result = await form_fields_collection.delete_one({"_id": ObjectId(field_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Form field not found")
        
    return {"message": "deleted"}
