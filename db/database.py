from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection string
MONGO_URI = "mongodb+srv://devlup:Parth0207@cluster0.wertdyf.mongodb.net/?appName=Cluster0"

# create client
client = AsyncIOMotorClient(MONGO_URI)

# select database
db = client["devlup"]

mentor_collection = db["mentors"]

