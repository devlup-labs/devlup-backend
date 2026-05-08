from fastapi import HTTPException
from server.database import stats_collection
from server.models.stats_model import StatModel
from server.schemas.stats_schema import StatCreate

async def record_new_visit(stat_data: StatCreate):
    stat_dict = stat_data.dict()
    new_stat = await stats_collection.insert_one(stat_dict)
    created_stat = await stats_collection.find_one({"_id": new_stat.inserted_id})
    return StatModel(**created_stat)

async def get_all_visits():
    visits = await stats_collection.find().to_list(100000)
    return [StatModel(**visit) for visit in visits]
