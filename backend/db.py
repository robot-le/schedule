from fastapi import Depends
from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from config import settings

client = AsyncIOMotorClient(settings.mongodb_uri)
db = client.myDatabase
collection = db.myCollection

async def get_collection() -> AsyncIOMotorCollection:
    return collection

CollectionDep = Annotated[AsyncIOMotorCollection, Depends(get_collection)]
