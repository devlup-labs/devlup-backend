from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection string
MONGO_URI = "mongodb+srv://devlup:Parth0207@cluster0.wertdyf.mongodb.net/?appName=Cluster0"

# create client
client = AsyncIOMotorClient(MONGO_URI)

# select database
db = client["devlup"]

# collections
project_collection = db["projects"]
mentor_collection = db["mentors"]
timeline_collection = db["timeline"]
application_collection = db["applications"]
preference_collection = db["application_preferences"]
stats_collection = db["stats"]
page_stats_collection = db["page_stats"]
project_mentor_collection = db["project_mentors"]