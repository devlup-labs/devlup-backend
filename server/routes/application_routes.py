from fastapi import APIRouter
from bson import ObjectId
from server.database import application_collection
from server.schemas.application_schema import Application

router = APIRouter()


@router.get("/applications")
async def get_applications():

    applications = []

    cursor = application_collection.find()

    async for a in cursor:
        a["_id"] = str(a["_id"])
        applications.append(a)

    return applications


@router.post("/applications")
async def create_application(application: Application):

    result = await application_collection.insert_one(application.dict())

    return {"application_id": str(result.inserted_id)}


@router.get("/applications/{application_id}")
async def get_application(application_id: str):

    app = await application_collection.find_one({"_id": ObjectId(application_id)})
    app["_id"] = str(app["_id"])

    return app


@router.delete("/applications/{application_id}")
async def delete_application(application_id: str):

    await application_collection.delete_one({"_id": ObjectId(application_id)})

    return {"message": "deleted"}