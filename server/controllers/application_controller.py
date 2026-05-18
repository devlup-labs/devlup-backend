from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
import requests
import os
import asyncio
from server.database import application_collection
from server.schemas.application_schema import ApplicationCreate, ApplicationUpdate

GOOGLE_SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")


async def send_to_google_script(application_data: dict):
    """
    Send application data to Google Apps Script asynchronously.
    This runs in the background and doesn't block the API response.
    Maps all application fields dynamically to the payload.
    """
    if not GOOGLE_SCRIPT_URL:
        print("Warning: GOOGLE_SCRIPT_URL not configured in .env")
        return

    try:
        # Create a payload with ALL fields from the application
        # This allows dynamic form fields to be included automatically
        payload = {}
        
        for key, value in application_data.items():
            # Skip internal fields and MongoDB ID
            if key not in ["_id", "id", "updated_at"]:
                # Convert datetime objects to strings for JSON serialization
                if hasattr(value, "isoformat"):
                    payload[key] = value.isoformat()
                else:
                    payload[key] = value

        # Send POST request to Google Apps Script
        response = requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=10)
        print(f"Google Script response: {response.status_code}")
        print(f"Payload sent: {payload}")
        
    except requests.exceptions.Timeout:
        print("Error: Google Apps Script request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to Google Apps Script: {str(e)}")
    except Exception as e:
        print(f"Unexpected error in send_to_google_script: {str(e)}")

async def get_applications_controller():
    applications = []
    cursor = application_collection.find()
    
    async for a in cursor:
        a["id"] = str(a["_id"])
        del a["_id"]
        applications.append(a)
        
    return applications

async def create_application_controller(application: ApplicationCreate, submitter_email: str = None):
    app_dict = application.model_dump()
    app_dict["created_at"] = datetime.utcnow()
    app_dict["updated_at"] = datetime.utcnow()
    if submitter_email:
        app_dict["submitter_email"] = submitter_email
    
    result = await application_collection.insert_one(app_dict)
    
    new_app = await application_collection.find_one({"_id": result.inserted_id})
    new_app["id"] = str(new_app["_id"])
    del new_app["_id"]
    
    # Send application data to Google Apps Script in the background (non-blocking)
    try:
        asyncio.create_task(send_to_google_script(app_dict))
    except Exception as e:
        print(f"Failed to queue Google Script task: {str(e)}")
    
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

async def get_application_by_email_controller(email: str):
    """Find an application by the submitter's email address. Returns None if not found."""
    app = await application_collection.find_one({"submitter_email": email})
    if not app:
        return None
    app["id"] = str(app["_id"])
    del app["_id"]
    return app

async def update_application_controller(application_id: str, application_update: ApplicationUpdate):
    if not ObjectId.is_valid(application_id):
        raise HTTPException(status_code=400, detail="Invalid application ID")
    update_data = {k: v for k, v in application_update.model_dump(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
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
