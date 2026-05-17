from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
PROJECTS_DB_NAME =os.getenv("PROJECTS_DB_NAME")
MAIN_DB_NAME =os.getenv("MAIN_DB_NAME")

client = AsyncIOMotorClient(MONGO_URI)

projects_db = client[PROJECTS_DB_NAME]
main_db = client[MAIN_DB_NAME]

project_collection = projects_db["projects"]
mentor_collection = projects_db["mentors"]
timeline_collection = projects_db["timeline"]
application_collection = projects_db["applications"]
# preference_collection = projects_db["application_preferences"]
stats_collection = projects_db["stats"]
# page_stats_collection = projects_db["page_stats"]
# project_mentor_collection = projects_db["project_mentors"]
form_fields_collection = projects_db["form_fields"]
user_collection = projects_db["users"]