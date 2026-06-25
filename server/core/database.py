from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
PROJECTS_DB_NAME =os.getenv("PROJECTS_DB_NAME")
MAIN_DB_NAME =os.getenv("MAIN_DB_NAME")

client_async = AsyncIOMotorClient(MONGO_URI)
client_sync = MongoClient(MONGO_URI)

projects_db = client_async[PROJECTS_DB_NAME]
main_db_async = client_async[MAIN_DB_NAME]
main_db_sync = client_sync[MAIN_DB_NAME]

project_collection = projects_db["projects"]
mentor_collection = projects_db["mentors"]
timeline_collection = projects_db["timeline"]
application_collection = projects_db["applications"]
# preference_collection = projects_db["application_preferences"]
stats_collection = projects_db["stats"]
# page_stats_collection = projects_db["page_stats"]
# project_mentor_collection = projects_db["project_mentors"]
form_fields_collection = projects_db["form_fields"]
projects_user_collection = projects_db["users"]
settings_collection = projects_db["settings"]

main_user_collection = main_db_async["users"]