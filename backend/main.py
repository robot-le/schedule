from typing import Annotated
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.myDatabase
collection = db.myCollection

PyObjectId = Annotated[str, BeforeValidator(str)]

class Schedule(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    person: str
    subject: str
    date_start: datetime = Field(default=datetime.today())
    date_finish: datetime = Field(default=datetime.today() + timedelta(days=10))
    model_config = ConfigDict(populate_by_name=True)

class ScheduleCollection(BaseModel):
    schedules: list[Schedule]

@app.post('/schedules')
async def create_schedule(item: Schedule):
    result = await collection.insert_one(item.model_dump())
    return {"id": str(result.inserted_id)}

@app.get("/schedules")
async def read_schedules():
    return ScheduleCollection(schedules=await collection.find().to_list(100))
