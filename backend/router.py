from db import CollectionDep
from schemas import Schedule, ScheduleCollection
from fastapi import APIRouter


router = APIRouter(prefix='/api')


@router.post(
        '/schedules',
        response_model=Schedule,
)
async def create_schedule(
    item: Schedule,
    collection: CollectionDep,
    ):
    existing_schedule = await collection.find_one({'person': item.person})
    if existing_schedule:
        result = await collection.find_one_and_update(
            {'person': item.person},
            {'$set': {
                'start_day': item.start_day,
                'end_day': item.end_day,
                'subject': item.subject,
            }},
            upsert=True,
            return_document=True,
        )
    else:
        new_schedule = await collection.insert_one(
            item.model_dump(by_alias=True, exclude={'id'})
        )
        doc_id = new_schedule.inserted_id
        result = await collection.find_one({'_id': doc_id})
        result['_id'] = str(result['_id'])

    return Schedule(**result)

@router.get(
        '/schedules',
        response_model=ScheduleCollection,
)
async def read_schedules(
    collection: CollectionDep,
):
    return ScheduleCollection(schedules=await collection.find().to_list(100))