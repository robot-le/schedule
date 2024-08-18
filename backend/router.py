from db import CollectionDep
from schemas import Schedule, ScheduleCollection
from fastapi import APIRouter


router = APIRouter()


@router.post('/schedules')
async def create_schedule(
    item: Schedule,
    collection: CollectionDep,
    ):
    result = await collection.insert_one(item.model_dump())
    return {'id': str(result.inserted_id)}

@router.get('/schedules')
async def read_schedules(
    collection: CollectionDep,
):
    return ScheduleCollection(schedules=await collection.find().to_list(100))