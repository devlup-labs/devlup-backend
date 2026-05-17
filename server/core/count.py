import asyncio
from database import stats_collection

async def count():
    c = await stats_collection.count_documents({})
    print(f"TOTAL: {c}")

if __name__ == "__main__":
    asyncio.run(count())
