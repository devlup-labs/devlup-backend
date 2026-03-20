from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME =os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URI)


db = client[DB_NAME]


# project_collection = db["projects"]
# mentor_collection = db["mentors"]
# timeline_collection = db["timeline"]
application_collection = db["applications"]
# preference_collection = db["application_preferences"]
stats_collection = db["stats"]
page_stats_collection = db["page_stats"]
# project_mentor_collection = db["project_mentors"]