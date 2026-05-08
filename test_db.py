import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

async def run():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["devlup"]
    collection = db["projects"]
    cursor = collection.find({"$or": [{"approval_status": "accepted"}, {"approval_status": {"$exists": False}}]})
    projects = await cursor.to_list(length=100)
    print(f"Total accepted projects: {len(projects)}")
    for p in projects:
        print(f"ID: {p.get('_id')} | Title: {p.get('project_title')} | Status: {p.get('status')} | Approval: {p.get('approval_status')}")

asyncio.run(run())
