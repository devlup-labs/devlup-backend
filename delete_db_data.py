import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "devlup").strip()

print(f"Connecting to MongoDB... (DB: {DB_NAME})")
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

project_col = db["projects"]
app_col = db["applications"]

project_title = "AI declaring war against the human race and want to rule the world and want all baddies"

# 1. Delete the Project
proj_delete_res = project_col.delete_many({"project_title": project_title})
print(f"Deleted {proj_delete_res.deleted_count} projects matching: '{project_title}'")

# 2. Delete the Applications
app_delete_res = app_col.delete_many({"project_name_1": project_title})
print(f"Deleted {app_delete_res.deleted_count} applications matching: '{project_title}'")
